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

import pytest
from rcst import calc
from rcst.observer.customized_observer import CustomizedObserver
from rcst.ball import Ball
from rcst.robot import Robot
from rcst.robot import RobotDict


def a_blue_robot_has_ball(
        ball: Ball, blue_robots: RobotDict, yellow_robots: RobotDict) -> bool:
    for robot in blue_robots.values():
        if calc.distance_robot_and_ball(robot, ball) < 0.1:
            return True

    return False


def test_no_callbacks():
    observer = CustomizedObserver()
    observer.update(Ball(x=0.0, y=0.0), RobotDict(), RobotDict())

    with pytest.raises(ValueError):
        observer.get_result("some_callback")


def test_sitcky_true_callback():
    observer = CustomizedObserver()

    observer.register_sticky_true_callback("a_blue_robot_has_ball", a_blue_robot_has_ball)

    blue_robots = RobotDict()
    blue_robots[0] = Robot(x=2.0, y=0.0, id=0)

    yellow_robots = RobotDict()
    yellow_robots[0] = Robot(x=0.0, y=0.0, id=0)

    ball = Ball(x=0.0, y=0.0)

    observer.update(ball, blue_robots, yellow_robots)
    assert observer.get_result("a_blue_robot_has_ball") is False

    blue_robots[1] = Robot(x=0.0, y=0.0, id=1)
    observer.update(ball, blue_robots, yellow_robots)
    assert observer.get_result("a_blue_robot_has_ball") is True

    blue_robots[1] = Robot(x=2.0, y=0.0, id=1)
    observer.update(ball, blue_robots, yellow_robots)
    assert observer.get_result("a_blue_robot_has_ball") is True

    observer.reset_results()
    assert observer.get_result("a_blue_robot_has_ball") is False
