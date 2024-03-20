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
from rcst.ball import Ball
import rcst.calc as calc
from rcst.robot import Robot


def test_distance():
    assert calc.distance(0, 0, 0, 0) == 0
    assert calc.distance(2, 3, -2, 3) == 4


def test_distance_robot_and_ball():
    robot = Robot(0, 0)
    ball = Ball(0, 0)

    assert calc.distance_robot_and_ball(robot, ball) == 0.0

    robot = Robot(1, 1)
    ball = Ball(2, 2)

    assert calc.distance_robot_and_ball(robot, ball) == pytest.approx(1.41421356)


def test_velocity_norm():
    prev = Robot(0, 0)
    present = Robot(0, 0)

    assert calc.velocity_norm(present, prev, 1) == 0.0

    prev = Robot(0, 0)
    present = Robot(2, 2)

    assert calc.velocity_norm(present, prev, 1) == 2.8284271247461903
    assert calc.velocity_norm(present, prev, 0.1) == 28.284271247461903

    with pytest.raises(ValueError):
        calc.velocity_norm(present, prev, 0.0)
