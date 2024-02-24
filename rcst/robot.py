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

from typing import List
from typing import TypeAlias

RobotDict: TypeAlias = dict[int, 'Robot']


class Robot:
    def __init__(self, x: float = 0.0, y: float = 0.0, orientation: float = 0.0,
                 is_yellow: bool = False, id: int = 0, turn_on: bool = True) -> None:
        self.x = x
        self.y = y
        self.orientation = orientation
        self.is_yellow = is_yellow
        self.id = id
        self.turn_on = turn_on

        self._v_x: List[float] = []
        self._v_y: List[float] = []
        self._v_angular: List[float] = []
        self._kick_speed_x: List[float] = []
        self._kick_speed_z: List[float] = []
        self._dribble: List[bool] = []

    def set_command(self, v_x: float, v_y: float, v_angular: float,
                    kick_speed_x: float, kick_speed_z, dribble: bool) -> None:
        self._v_x = [v_x]
        self._v_y = [v_y]
        self._v_angular = [v_angular]
        self._kick_speed_x = [kick_speed_x]
        self._kick_speed_z = [kick_speed_z]
        self._dribble = [dribble]

    def has_command(self) -> bool:
        return len(self._v_x) and len(self._v_y) and len(self._v_angular) \
               and len(self._kick_speed_x) and len(self._kick_speed_z) and len(self._dribble)
