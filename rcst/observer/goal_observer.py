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

from ..ball import Ball


class GoalObserver:
    """
    Observes which side has scored a goal.
    """
    def __init__(self, field_half_length: float, goal_half_width: float,
                 goal_depth: float):
        self._field_half_length = field_half_length
        self._goal_half_width = goal_half_width
        self._goal_depth = goal_depth

        self._ball_has_been_in_positive_goal = False
        self._ball_has_been_in_negative_goal = False

    def update(self, ball: Ball) -> None:
        if not self._ball_has_been_in_positive_goal:
            self._ball_has_been_in_positive_goal = self._ball_in_positive_goal(ball)

        if not self._ball_has_been_in_negative_goal:
            self._ball_has_been_in_negative_goal = self._ball_in_negative_goal(ball)

    def reset(self) -> None:
        self._ball_has_been_in_positive_goal = False
        self._ball_has_been_in_negative_goal = False

    def ball_has_been_in_positive_goal(self) -> bool:
        return self._ball_has_been_in_positive_goal

    def ball_has_been_in_negative_goal(self) -> bool:
        return self._ball_has_been_in_negative_goal

    def _ball_in_positive_goal(self, ball: Ball) -> bool:
        in_goal_depth = ball.x > self._field_half_length \
                        and ball.x < self._field_half_length + self._goal_depth
        in_goal_width = abs(ball.y) < self._goal_half_width
        return in_goal_depth and in_goal_width

    def _ball_in_negative_goal(self, ball: Ball) -> bool:
        in_goal_depth = ball.x < -self._field_half_length \
                        and ball.x > -self._field_half_length - self._goal_depth
        in_goal_width = abs(ball.y) < self._goal_half_width
        return in_goal_depth and in_goal_width

