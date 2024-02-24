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

from .vision_world import VisionWorld
from .observer.goal_observer import GoalObserver

from typing_extensions import deprecated


class WorldObserver:
    """
    Observes the world and updates the state of the world.
    """
    def __init__(self, field_length: float = 12.0, field_width: float = 9.0,
                 goal_width: float = 1.8, goal_depth: float = 0.18):
        self._field_length = field_length
        self._field_half_length = field_length / 2.0
        self._field_width = field_width
        self._goal_width = goal_width
        self._goal_half_width = goal_width / 2.0
        self._goal_depth = goal_depth

        self._vision_world = VisionWorld()

        self._goal_observer = GoalObserver(
            self._field_half_length, self._goal_half_width, self._goal_depth)

    def update(self, vision_world: VisionWorld) -> None:
        self._vision_world = vision_world
        ball = self._vision_world.get_ball()
        self._goal_observer.update(ball)

    def reset(self) -> None:
        self._goal_observer.reset()

    def goal(self) -> GoalObserver:
        return self._goal_observer

    @deprecated('ball_has_been_in_positive_goal() is moved to goal(). Use goal() instead.')
    def ball_has_been_in_positive_goal(self) -> bool:
        return self._goal_observer.ball_has_been_in_positive_goal()

    @deprecated('ball_has_been_in_negative_goal() is moved to goal(). Use goal() instead.')
    def ball_has_been_in_negative_goal(self) -> bool:
        return self._goal_observer.ball_has_been_in_negative_goal()

    def get_world(self) -> VisionWorld:
        return self._vision_world
