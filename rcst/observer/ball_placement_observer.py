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
from ..robot import RobotDict
from .. import calc


class BallPlacementObserver:
    """
    Observes the placement of the ball in the field
    """
    def __init__(self):
        self._target_x = 0.0
        self._target_y = 0.0
        self._for_blue_team_placement = True
        self._success = False

    def update(self, ball: Ball, blue_robots: RobotDict, yellow_robots: RobotDict) -> None:
        # Ref: https://robocup-ssl.github.io/ssl-rules/sslrules.html#_ball_placement
        if not self._ball_is_in_target_position(ball):
            self._success = False
            return

        blue_distance = 0.05 if self._for_blue_team_placement else 0.5
        yellow_distance = 0.5 if self._for_blue_team_placement else 0.05

        if not self._no_robots_are_nearby(blue_robots, blue_distance):
            self._success = False
            return

        if not self._no_robots_are_nearby(yellow_robots, yellow_distance):
            self._success = False
            return
        
        self._success = True

    def reset(self) -> None:
        self._target_x = 0.0
        self._target_y = 0.0
        self._for_blue_team_placement = True
        self._success = False

    def set_targets(self, pos_x: float, pos_y: float, for_blue_team: bool) -> None:
        self._target_x = pos_x
        self._target_y = pos_y
        self._for_blue_team_placement = for_blue_team

    def success(self) -> bool:
        return self._success

    def _ball_is_in_target_position(self, ball: Ball) -> bool:
        if calc.distance(ball.x, ball.y, self._target_x, self._target_y) <= 0.15:
            return True
        return False

    def _no_robots_are_nearby(self, robots: RobotDict, distance: float) -> bool:
        for robot in robots.values():
            if calc.distance(robot.x, robot.y, self._target_x, self._target_y) <= distance:
                return False
        return True
