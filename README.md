
# Simple RoboCup SSL Library

[![Python application](https://github.com/SSL-Roots/simple_robocup_ssl/actions/workflows/python-app.yml/badge.svg)](https://github.com/SSL-Roots/simple_robocup_ssl/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/SSL-Roots/simple_robocup_ssl/graph/badge.svg?token=8MWSNFAOG9)](https://codecov.io/gh/SSL-Roots/simple_robocup_ssl)

Simple python library for RoboCup SSL (`srssl`).

## Requirements

- [Google Protobuf Compiler](https://github.com/protocolbuffers/protobuf)
  - The `protoc` command is required during `srssl` installation.

## Installation

```bash
# Install Google Protobuf Compiler
sudo apt install protobuf-compiler

# Install srssl
pip install git+https://github.com/SSL-Roots/simple_robocup_ssl
```

## Linting

This project uses [flake8](https://flake8.pycqa.org/en/latest/) for linting.

Settings for flake8 are in [setup.cfg](setup.cfg).

```bash
cd simple_robocup_ssl
flake8 .
```

## License

Apache License 2.0
