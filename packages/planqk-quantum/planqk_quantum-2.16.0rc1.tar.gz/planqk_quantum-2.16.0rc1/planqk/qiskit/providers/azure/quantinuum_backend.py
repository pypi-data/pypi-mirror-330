import logging
from typing import Dict, Any, List, Union

import pyqir
from qiskit import QuantumCircuit
from qsharp import TargetProfile
from qsharp.interop.qiskit import QSharpBackend

from planqk.client.model_enums import JobInputFormat
from planqk.qiskit.options import OptionsV2
from planqk.qiskit.provider import PlanqkQuantumProvider
from planqk.qiskit.providers.azure.azure_backend import PlanqkAzureQiskitBackend

logger = logging.getLogger(__name__)

class CallableStr(str):
    def __call__(self):
        return self

@PlanqkQuantumProvider.register_backend("azure.quantinuum.h1")
class PlanqkAzureQuantinuumBackend(PlanqkAzureQiskitBackend):

    @classmethod
    def _default_options(cls):
        return OptionsV2()

    @property
    def name(self):
        return CallableStr(self._name)

    @name.setter
    def name(self, value):
        self._name = value


    def _get_job_input_format(self) -> JobInputFormat:
        return JobInputFormat.QIR_V1

    def _convert_to_job_input(self, job_input, options=None):
        input_params: Dict[str, Any] = vars(self.options).copy()
        return self._translate_input(job_input, input_params)


    def _convert_to_job_params(self, job_input: QuantumCircuit = None, options=None) -> dict:
        input_params: Dict[str, Any] = vars(self.options).copy()
        if not (isinstance(job_input, list)):
            circuits = [job_input]

        def get_func_name(func: pyqir.Function) -> str:
            return func.name

        target_profile = self._get_target_profile(input_params)

        module = self._generate_qir(
            circuits, target_profile, skip_transpilation=True
        )

        entry_points = list(
            map(get_func_name, filter(pyqir.is_entry_point, module.functions))
        )

        if "items" not in input_params:
            arguments = input_params.pop("arguments", [])
            input_params["items"] = [
                {"entryPoint": name, "arguments": arguments} for name in entry_points
            ]

        input_params.update({"num_qubits": job_input.num_qubits, "qiskit": 'True'})

        return input_params

    def _generate_qir(
            self, circuits: List[QuantumCircuit], target_profile: any, **kwargs
    ) -> pyqir.Module:

        if len(circuits) == 0:
            raise ValueError("No QuantumCircuits provided")

        config = self.configuration()
        # Barriers aren't removed by transpilation and must be explicitly removed in the Qiskit to QIR translation.
        supports_barrier = "barrier" in config.basis_gates
        skip_transpilation = kwargs.pop("skip_transpilation", False)

        backend = QSharpBackend(
            qiskit_pass_options={"supports_barrier": supports_barrier},
            target_profile=target_profile,
            skip_transpilation=skip_transpilation,
            **kwargs,
        )

        name = "batch"
        if len(circuits) == 1:
            name = circuits[0].name

        if isinstance(circuits, list):
            for value in circuits:
                if not isinstance(value, QuantumCircuit):
                    raise ValueError("Input must be List[QuantumCircuit]")
        else:
            raise ValueError("Input must be List[QuantumCircuit]")

        context = pyqir.Context()
        llvm_module = pyqir.qir_module(context, name)
        for circuit in circuits:
            qir_str = backend.qir(circuit)
            module = pyqir.Module.from_ir(context, qir_str)
            entry_point = next(filter(pyqir.is_entry_point, module.functions))
            entry_point.name = circuit.name
            llvm_module.link(module)
        err = llvm_module.verify()
        if err is not None:
            raise Exception(err)

        return llvm_module

    def _get_qir_str(
            self,
            circuits: List[QuantumCircuit],
            target_profile: TargetProfile,
            **to_qir_kwargs,
    ) -> str:
        module = self._generate_qir(circuits, target_profile, **to_qir_kwargs)
        return str(module)

    def _get_target_profile(self, input_params) -> TargetProfile:
        default_profile = self.options.get("target_profile", TargetProfile.Adaptive_RI)
        return input_params.pop("target_profile", default_profile)

    def _translate_input(
            self, circuits: Union[QuantumCircuit, List[QuantumCircuit]], input_params: Dict[str, Any]
    ) -> str:
        """
        Translates the input values to the QIR expected by the Backend.

        Adapted from the azure-quantum-python aws_quantum_task.py module.

        Original source:
        Azure Quantum Python SDK for Python (MIT License)
        GitHub Repository: https://github.com/microsoft/azure-quantum-python/blob/main/azure-quantum/azure/quantum/qiskit/backends/backend.py
        """
        logger.info("Using QIR as the job's payload format.")
        if not (isinstance(circuits, list)):
            circuits = [circuits]

        target_profile = self._get_target_profile(input_params)

        if logger.isEnabledFor(logging.DEBUG):
            qir = self._get_qir_str(circuits, target_profile, skip_transpilation=True)
            logger.debug(f"QIR:\n{qir}")

        # We'll transpile automatically to the supported gates in QIR unless explicitly skipped.
        skip_transpilation = input_params.pop("skipTranspile", False)

        module = self._generate_qir(
            circuits, target_profile, skip_transpilation=skip_transpilation
        )

        if not skip_transpilation:
            # We'll only log the QIR again if we performed a transpilation.
            if logger.isEnabledFor(logging.DEBUG):
                qir = str(module)
                logger.debug(f"QIR (Post-transpilation):\n{qir}")

        return str(module)