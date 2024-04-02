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


def calc_vector(x0: float, y0: float, x1: float, y1: float) -> tuple[float, float]:
    return x1-x0, y1-y0


def distance_line_ab_to_point_c(xa: float, ya: float, xb: float, yb: float, xc: float, yc: float) -> float:
    ACx, ACy = calc_vector(xa, ya, xc, yc)
    ABx, ABy = calc_vector(xa, ya, xb, yb)
    BCx, BCy = calc_vector(xb, yb, xc, yc)
    BAx, BAy = calc_vector(xb, yb, xa, ya)

    ab_is_not_line = False
    if xa == xb and ya == yb:
        ab_is_not_line = True

    # AB is point or point C is the A side
    if ab_is_not_line or ACx * ABx + ACy * ABy < 0:
        return (ACx * ACx + ACy * ACy)**0.5
    # Point C is the B side
    if BCx * BAx + BCy * BAy < 0:
        return (BCx * BCx + BCy * BCy)**0.5

    v_s = abs(ACx * ABy - ACy * ABx)
    v_l = (ABx * ABx + ABy * ABy)**0.5
    return v_s/v_l
