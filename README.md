
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
pip install -v git+https://github.com/SSL-Roots/robocup_scenario_test
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

    assert rcst_comm.observer.goal().ball_has_been_in_positive_goal() is True
```

More examples are in [tests](tests).

### Logging

This library supports the `ssl-log-recorder` of [ssl-go-tools](https://github.com/RoboCup-SSL/ssl-go-tools/tree/master).

You can record logs on the GitHub Actions like this:

```yaml
- name: Download logger
  run: |
    curl -L https://github.com/RoboCup-SSL/ssl-go-tools/releases/download/v1.5.2/ssl-log-recorder_v1.5.2_linux_amd64 -o ssl-log-recorder
    chmod +x ssl-log-recorder

- name: Run scenario tests
  run: pytest tests/test_scenario_*.py --vision_port=10020 --logging --log_recorder=./ssl-log-recorder
```

When a test fails, the library saves the log file as `TEST_NAME.log.gz` in the current directory.

Please see GitHub workflow examples in [`.github/workflows`](.github/workflows).

## Linting

This project uses [flake8](https://flake8.pycqa.org/en/latest/) for linting.

Settings for flake8 are in [setup.cfg](setup.cfg).

```bash
cd robocup_scenario_test
flake8 .
```

## License

Apache License 2.0
