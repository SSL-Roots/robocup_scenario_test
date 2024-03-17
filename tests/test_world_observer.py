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

from rcst.ball import Ball
from rcst.robot import Robot
from rcst.vision_world import VisionWorld
from rcst.world_observer import WorldObserver

import time


def test_goal_instance():
    # Note: The goal observer's tests are already covered in the test_goal_observer.py file.
    observer = WorldObserver(
        field_length=12.0, field_width=9.0, goal_width=1.8, goal_depth=0.18)

    vision_world = VisionWorld()
    vision_world._ball = [Ball(x=6.01, y=0.0)]
    observer.update(vision_world)

    assert observer.goal().ball_has_been_in_positive_goal() is True

    observer.reset()
    assert observer.goal().ball_has_been_in_positive_goal() is False


def test_ball_placement():
    # Note: The ball placement observer's tests are already covered in
    # the test_ball_placement_observer.py file.
    observer = WorldObserver(
        field_length=12.0, field_width=9.0, goal_width=1.8, goal_depth=0.18)

    vision_world = VisionWorld()
    vision_world._ball = [Ball(x=1.0, y=2.0)]

    observer.ball_placement().set_targets(1.0, 2.0, for_blue_team=True)

    observer.update(vision_world)
    assert observer.ball_placement().success() is True

    observer.reset()
    assert observer.ball_placement().success() is False


def test_robot_speed():
    # Note: The robot speed observer's tests are already covered in
    # the test_robot_speed_observer.py file.
    observer = WorldObserver(
        field_length=12.0, field_width=9.0, goal_width=1.8, goal_depth=0.18)

    vision_world = VisionWorld()
    vision_world._blue_robots[0] = Robot(x=0.0, y=0.0, id=0)
    vision_world._yellow_robots[0] = Robot(x=0.0, y=0.0, id=0)
    observer.update(vision_world)

    time.sleep(1)  # This makes dt = 1.0
    vision_world._blue_robots[0] = Robot(x=1.0, y=0.0, id=0)
    vision_world._yellow_robots[0] = Robot(x=1.0, y=0.0, id=0)
    observer.update(vision_world)
    assert observer.robot_speed().some_blue_robots_over(0.1) is True
    assert observer.robot_speed().some_yellow_robots_over(0.1) is True

    observer.reset()
    assert observer.robot_speed().some_blue_robots_over(0.1) is False
    assert observer.robot_speed().some_yellow_robots_over(0.1) is False
