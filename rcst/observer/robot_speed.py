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

from copy import deepcopy

from ..robot import RobotDict
from .. import calc


class RobotSpeedObserver:
    """
    Observes the speed of the robots
    """
    def __init__(self):
        self._prev_blue_robots = RobotDict()
        self._prev_yellow_robots = RobotDict()
        self._blue_max_velocities: dict[int, float] = {}
        self._yellow_max_velocities: dict[int, float] = {}

        self._prev_timestamp = -1.0

    def update(self, blue_robots: RobotDict, yellow_robots: RobotDict, timestamp: float) -> None:
        if timestamp <= self._prev_timestamp:
            return

        dt = timestamp - self._prev_timestamp
        self._prev_timestamp = timestamp

        self._update_max_velocity(
            blue_robots, self._prev_blue_robots, self._blue_max_velocities, dt)
        self._update_max_velocity(
            yellow_robots, self._prev_yellow_robots, self._yellow_max_velocities, dt)

        self._prev_blue_robots = deepcopy(blue_robots)
        self._prev_yellow_robots = deepcopy(yellow_robots)

    def reset(self) -> None:
        self._prev_blue_robots = RobotDict()
        self._prev_yellow_robots = RobotDict()
        self._blue_max_velocities: dict[int, float] = {}
        self._yellow_max_velocities: dict[int, float] = {}

    def blue_max_velocities(self) -> dict[int, float]:
        return self._blue_max_velocities

    def yellow_max_velocities(self) -> dict[int, float]:
        return self._yellow_max_velocities

    def _robot_over(
            self, robot_id: int, velocity: float,
            max_velocities: dict[int, float]) -> bool:
        if robot_id not in max_velocities.keys():
            return False
        return max_velocities[robot_id] > velocity

    def blue_robot_over(self, robot_id: int, velocity: float) -> bool:
        return self._robot_over(robot_id, velocity, self._blue_max_velocities)

    def yellow_robot_over(self, robot_id: int, velocity: float) -> bool:
        return self._robot_over(robot_id, velocity, self._yellow_max_velocities)

    def _some_robots_over(
            self, max_velocities: dict[int, float], velocity: float) -> bool:
        for v in max_velocities.values():
            if v > velocity:
                return True
        return False

    def some_blue_robots_over(self, velocity: float) -> bool:
        return self._some_robots_over(self._blue_max_velocities, velocity)

    def some_yellow_robots_over(self, velocity: float) -> bool:
        return self._some_robots_over(self._yellow_max_velocities, velocity)

    def _update_max_velocity(
            self, robots: RobotDict, prev_robots: RobotDict,
            max_velocities: dict[int, float], dt: float) -> None:

        for robot in robots.values():
            if robot.id not in prev_robots.keys():
                continue

            velocity = calc.velocity_norm(robot, prev_robots[robot.id], dt)
            if robot.id not in max_velocities.keys():
                max_velocities[robot.id] = velocity
                continue

            if velocity > max_velocities[robot.id]:
                max_velocities[robot.id] = velocity
