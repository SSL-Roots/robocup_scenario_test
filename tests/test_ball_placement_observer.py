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

from rcst.observer.ball_placement_observer import BallPlacementObserver
from rcst.ball import Ball
from rcst.robot import Robot
from rcst.robot import RobotDict


def test_ball_is_in_target_position():
    placement = BallPlacementObserver()

    blue_robots = RobotDict()
    yellow_robots = RobotDict()

    placement.set_targets(2.0, -2.0, for_blue_team=True)
    placement.update(Ball(x=2.15, y=-2.0), blue_robots, yellow_robots)
    assert placement.success() is True

    placement.update(Ball(x=2.0, y=-2.15), blue_robots, yellow_robots)
    assert placement.success() is True

    placement.update(Ball(x=2.16, y=-2.0), blue_robots, yellow_robots)
    assert placement.success() is False

    placement.update(Ball(x=2.0, y=-2.16), blue_robots, yellow_robots)
    assert placement.success() is False

    placement.update(Ball(x=2.0, y=-2.0), blue_robots, yellow_robots)
    assert placement.success() is True

    placement.reset()
    assert placement.success() is False


def test_for_blue_team():
    placement = BallPlacementObserver()

    ball = Ball(x=0.0, y=0.0)
    blue_robots = RobotDict()
    yellow_robots = RobotDict()

    placement.set_targets(0.0, 0.0, for_blue_team=True)

    blue_robots[0] = Robot(x=0.06, y=0.0)
    placement.update(ball, blue_robots, yellow_robots)
    assert placement.success() is True

    blue_robots[1] = Robot(x=0.05, y=0.0)
    placement.update(ball, blue_robots, yellow_robots)
    assert placement.success() is False

    blue_robots[1] = Robot(x=0.06, y=0.0)
    yellow_robots[0] = Robot(x=0.0, y=0.6)
    placement.update(ball, blue_robots, yellow_robots)
    assert placement.success() is True

    yellow_robots[1] = Robot(x=0.0, y=0.5)
    placement.update(ball, blue_robots, yellow_robots)
    assert placement.success() is False


def test_for_yellow_team():
    placement = BallPlacementObserver()

    ball = Ball(x=0.0, y=0.0)
    blue_robots = RobotDict()
    yellow_robots = RobotDict()

    placement.set_targets(0.0, 0.0, for_blue_team=False)

    yellow_robots[0] = Robot(x=0.06, y=0.0)
    placement.update(ball, blue_robots, yellow_robots)
    assert placement.success() is True

    yellow_robots[1] = Robot(x=0.05, y=0.0)
    placement.update(ball, blue_robots, yellow_robots)
    assert placement.success() is False

    yellow_robots[1] = Robot(x=0.06, y=0.0)
    blue_robots[0] = Robot(x=0.0, y=0.6)
    placement.update(ball, blue_robots, yellow_robots)
    assert placement.success() is True

    blue_robots[1] = Robot(x=0.0, y=0.5)
    placement.update(ball, blue_robots, yellow_robots)
    assert placement.success() is False
