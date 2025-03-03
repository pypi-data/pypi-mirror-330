# QT Build Utils

[![PyPI version](https://badge.fury.io/py/qt-build-utils.svg)](https://pypi.org/project/qt-build-utils)

An utility to facilitate the building of Qt based projects

## Installation

### From PyPI

Install the package directly from PyPI using pip:

```bash
pip install qt-build-utils
```

### From Source

Clone the repository and install dependencies:

```bash
git clone https://fvsolutions-common/qt-build-utils.git
pip install -e qt-build-utils
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
Edit ui in designer

```sh
qt-build-utils edit [ui_file]
```

Convert ui to py

```sh
qt-build-utils convert [ui_file] -i
```