
# RoboCup Scenario Test Python Library

[![Python application](https://github.com/SSL-Roots/simple_robocup_ssl/actions/workflows/python-app.yml/badge.svg)](https://github.com/SSL-Roots/simple_robocup_ssl/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/SSL-Roots/robocup_scenario_test/graph/badge.svg?token=8MWSNFAOG9)](https://codecov.io/gh/SSL-Roots/robocup_scenario_test)

Python library for RoboCup SSL scenario test.

The library name `rcst` stands for "RoboCup Scenario Test".

## Requirements

- [Google Protobuf Compiler](https://github.com/protocolbuffers/protobuf)
  - The `protoc` command is required during `rcst` installation.

## Installation

```bash
# Install Google Protobuf Compiler
sudo apt install protobuf-compiler

# Install rcst
pip install git+https://github.com/SSL-Roots/robocup_scenario_test
```

## Usage

This library provides a plugin for [pytest](https://docs.pytest.org/en/stable/).

So, you can test your scenario like this:

```python
import math
import time


def test_our_kickoff(rcst_comm):
    rcst_comm.send_empty_world()
    rcst_comm.send_ball(0, 0)
    rcst_comm.send_blue_robot(1, -0.5, 0.0, math.radians(0))
    time.sleep(3)  # Wait for the robots to be placed.

    rcst_comm.observer.reset()
    rcst_comm.change_referee_command('STOP', 3.0)
    rcst_comm.change_referee_command('PREPARE_KICKOFF_BLUE', 3.0)
    rcst_comm.change_referee_command('NORMAL_START', 5.0)

    assert rcst_comm.observer.ball_has_been_in_positive_goal() is True
```

More examples are in [examples](examples).

## Linting

This project uses [flake8](https://flake8.pycqa.org/en/latest/) for linting.

Settings for flake8 are in [setup.cfg](setup.cfg).

```bash
cd robocup_scenario_test
flake8 .
```

## License

Apache License 2.0
