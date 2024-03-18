# Copyright 2024 Roots
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rcst.observer.robot_speed import RobotSpeedObserver
from rcst.robot import Robot
from rcst.robot import RobotDict

import pytest


def test_blue_robots_over():
    robot_speed = RobotSpeedObserver()

    blue_robots = RobotDict()
    blue_robots[0] = Robot(x=0.0, y=0.0, id=0)
    blue_robots[1] = Robot(x=0.0, y=0.0, id=1)

    yellow_robots = RobotDict()

    robot_speed.update(blue_robots, yellow_robots, timestamp=0.0)

    blue_robots[0] = Robot(x=1.0, y=0.0, id=0)
    blue_robots[1] = Robot(x=0.0, y=2.0, id=1)
    robot_speed.update(blue_robots, yellow_robots, timestamp=1.0)

    assert robot_speed.blue_max_velocities()[0] == pytest.approx(1.0, abs=0.01)
    assert robot_speed.blue_max_velocities()[1] == pytest.approx(2.0, abs=0.01)

    assert robot_speed.some_blue_robots_over(0.9) is True
    assert robot_speed.some_blue_robots_over(1.9) is True
    assert robot_speed.some_blue_robots_over(2.9) is False

    assert robot_speed.blue_robot_over(0, 0.9) is True
    assert robot_speed.blue_robot_over(0, 1.9) is False

    assert robot_speed.blue_robot_over(1, 1.9) is True
    assert robot_speed.blue_robot_over(1, 2.9) is False

    assert robot_speed.some_yellow_robots_over(0.9) is False

    robot_speed.reset()
    assert robot_speed.some_blue_robots_over(0.9) is False


def test_yelow_robots_over():
    robot_speed = RobotSpeedObserver()

    yellow_robots = RobotDict()
    yellow_robots[0] = Robot(x=0.0, y=0.0, id=0)
    yellow_robots[1] = Robot(x=0.0, y=0.0, id=1)

    blue_robots = RobotDict()

    robot_speed.update(blue_robots, yellow_robots, timestamp=0.0)

    # Robots are positioned at negative x and y
    yellow_robots[0] = Robot(x=-1.0, y=0.0, id=0)
    yellow_robots[1] = Robot(x=0.0, y=-2.0, id=1)
    robot_speed.update(blue_robots, yellow_robots, timestamp=1.0)

    assert robot_speed.yellow_max_velocities()[0] == pytest.approx(1.0, abs=0.01)
    assert robot_speed.yellow_max_velocities()[1] == pytest.approx(2.0, abs=0.01)

    assert robot_speed.some_yellow_robots_over(0.9) is True
    assert robot_speed.some_yellow_robots_over(1.9) is True
    assert robot_speed.some_yellow_robots_over(2.9) is False

    assert robot_speed.yellow_robot_over(0, 0.9) is True
    assert robot_speed.yellow_robot_over(0, 1.9) is False

    assert robot_speed.yellow_robot_over(1, 1.9) is True
    assert robot_speed.yellow_robot_over(1, 2.9) is False

    assert robot_speed.some_blue_robots_over(0.9) is False

    robot_speed.reset()
    assert robot_speed.some_yellow_robots_over(0.9) is False
