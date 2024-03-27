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
from .ball import Ball


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def distance_robot_and_ball(robot: Robot, ball: Ball) -> float:
    return distance(robot.x, robot.y, ball.x, ball.y)


def velocity_norm(present: Robot, previous: Robot, dt: float) -> float:
    if dt == 0:
        raise ValueError("dt cannot be zero")

    vx = (present.x - previous.x) / dt
    vy = (present.y - previous.y) / dt
    return math.sqrt(vx**2 + vy**2)


def distance_point_c_to_line_ab(xa: float, ya: float, xb: float, yb: float, xc: float, yc: float) -> float:
    # 線分ABの方程式: y - ya = (yb - ya) / (xb - xa) * (x - xa)
    if xb - xa == 0:  # 線分が垂直の場合
        return abs(xc - xa)
    
    a = (yb - ya) / (xb - xa)
    b = ya - a * xa
    
    # 点Cから線分ABまでの距離d
    d = abs(a * xc - yc + b) / math.sqrt(a**2 + 1)
    
    # 点Cが線分AB上にある場合
    if d == 0:
        x4 = xa + (xc - xa) * (xb - xa) / ((xb - xa)**2 + (yb - ya)**2)
        y4 = ya + (xc - xa) * (yb - ya) / ((xb - xa)**2 + (yb - ya)**2)
        d = math.sqrt((xc - x4)**2 + (yc - y4)**2)
    
    # 点Cが延長線上にある場合
    elif d > math.sqrt((xc - xa)**2 + (yc - ya)**2) or d > math.sqrt((xc - xb)**2 + (yc - yb)**2):
        d = min(math.sqrt((xc - xa)**2 + (yc - ya)**2), math.sqrt((xc - xb)**2 + (yc - yb)**2))
    
    return d
