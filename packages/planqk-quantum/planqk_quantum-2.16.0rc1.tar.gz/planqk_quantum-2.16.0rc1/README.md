# PLANQK Quantum SDK

[![PyPI version](https://badge.fury.io/py/planqk-quantum.svg)](https://badge.fury.io/py/planqk-quantum)

The PLANQK Quantum SDK is for developing quantum circuits using [Qiskit](https://pypi.org/project/qiskit) to be run on
quantum devices provided by the [PLANQK Platform](https://docs.planqk.de).
This library is an **extension** for Qiskit.
This means that you are able to seamlessly integrate and reuse your existing Qiskit code, leveraging the power and
familiarity of a framework you are already accustomed to.

## Getting Started

Check out the following guides on how to get started with PLANQK:

- [PLANQK Quickstart Guide](https://docs.planqk.de/quickstart.html)
- [Using the PLANQK Quantum SDK](https://docs.planqk.de/using-sdk.html)

## Installation

The package is released on PyPI and can be installed via `pip`:

```bash
pip install --upgrade planqk-quantum
```

To install a pre-release version, use the following command:

```bash
pip install --pre --upgrade planqk-quantum
```

## Development

To create a new Conda environment, run:

```bash
conda env create -f environment.yml
```

Then, to activate the environment:

```bash
conda activate planqk-quantum
```

To install the package in development mode, run:

```bash
pip install -e .
```

To update the environment, run:

```bash
conda env update -f environment.yml
```
