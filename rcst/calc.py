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

import math
from .robot import Robot


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def velocity_norm(present: Robot, previous: Robot, dt: float) -> float:
    if dt == 0:
        raise ValueError("dt cannot be zero")

    vx = (present.x - previous.x) / dt
    vy = (present.y - previous.y) / dt
    return math.sqrt(vx**2 + vy**2)
