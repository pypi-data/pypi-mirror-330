# FBS Build Utils

[![PyPI version](https://badge.fury.io/py/fbs-build-utils.svg)](https://pypi.org/project/fbs-build-utils)

An utility to facilitate the building of fman build system based projects

## Installation

### From PyPI

Install the package directly from PyPI using pip:

```bash
pip install fbs-build-utils
```

### From Source

Clone the repository and install dependencies:

```bash
git clone https://fvsolutions-common/fbs-build-utils.git
pip install -e fbs-build-utils
```

## Development

This project depends on UV for managing dependencies.
Make sure you have UV installed and set up in your environment.

You can find more information about UV [here](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv venv
```

```bash
uv sync --all-extras --dev
```

## Usage

Commands:
* build
* generate
* run
* run-installer
* run-python