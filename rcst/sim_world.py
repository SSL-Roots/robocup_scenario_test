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
from typing import List
from typing import Dict

from .ball import Ball
from .robot import Robot

from .proto.grsim import grSim_Packet_pb2 as grsim_packet
from .proto.grsim.grSim_Replacement_pb2 import grSim_Replacement
from .proto.grsim.grSim_Replacement_pb2 import grSim_RobotReplacement
from .proto.grsim.grSim_Replacement_pb2 import grSim_BallReplacement


class SimWorld:
    MAX_ROBOT_NUM = 11

    def __init__(self, field_length: float = 12.0, field_width: float = 9.0):
        self._ball: List[Ball] = []
        self._blue_robots: Dict[int, Robot] = {}
        self._yellow_robots: Dict[int, Robot] = {}
        self._field_length = field_length
        self._field_width = field_width

    @classmethod
    def make_empty_world(cls) -> 'SimWorld':
        """
        Make an empty world.
        All robots are turned off.
        Ball is placed at (0, 0).
        """
        world = cls()

        OFFSET_X = 0.2
        POS_X = 0.0
        BLUE_POS_Y = -world._field_width / 2.0 - 0.5
        YELLOW_POS_Y = BLUE_POS_Y - 0.2

        world._ball = [Ball()]
        world._blue_robots = world._all_robots_turn_off(
            False, POS_X, BLUE_POS_Y, OFFSET_X, 0.0)
        world._yellow_robots = world._all_robots_turn_off(
            True, POS_X, YELLOW_POS_Y, OFFSET_X, 0.0)
        return world

    def to_grsim_packet_string(self) -> bytes:
        """
        Convert this world to a grSim packet string.
        """
        packet = grsim_packet.grSim_Packet()
        packet.replacement.CopyFrom(self._to_grsim_replacement())
        return packet.SerializeToString()

    def set_ball(self, x: float, y: float, v_x: float = 0.0, v_y: float = 0.0) -> None:
        """
        Set ball position and velocity.
        """
        self._ball = [Ball(x, y, v_x, v_y)]

    def set_blue_robot(self, robot_id: int, x: float, y: float, orientation: float) -> None:
        """
        Set blue robot position and orientation.
        """
        self._set_robot(robot_id, False, x, y, orientation)

    def set_yellow_robot(self, robot_id: int, x: float, y: float, orientation: float) -> None:
        """
        Set yellow robot position and orientation.
        """
        self._set_robot(robot_id, True, x, y, orientation)

    def _set_robot(self, robot_id: int, is_yellow: bool,
                   x: float, y: float, orientation: float) -> None:
        robot = Robot(id=robot_id, is_yellow=is_yellow, turn_on=True,
                      x=x, y=y, orientation=orientation)
        if is_yellow:
            self._yellow_robots[robot_id] = robot
        else:
            self._blue_robots[robot_id] = robot

    def _all_robots_turn_off(self, is_yellow, x, y, offset_x, offset_y) -> Dict[int, Robot]:
        robots = {}
        for i in range(self.MAX_ROBOT_NUM):
            pos_x = x + i * offset_x
            pos_y = y + i * offset_y
            robots[i] = Robot(id=i, turn_on=False, is_yellow=is_yellow, x=pos_x, y=pos_y)
        return robots

    def _to_grsim_replacement(self) -> grSim_Replacement:
        replacement = grSim_Replacement()
        for robot in self._blue_robots.values():
            replacement.robots.extend([self._to_grsim_replacement_robot(robot)])
        for robot in self._yellow_robots.values():
            replacement.robots.extend([self._to_grsim_replacement_robot(robot)])
        for ball in self._ball:
            replacement.ball.CopyFrom(self._to_grsim_replacement_ball(ball))
        return replacement

    def _to_grsim_replacement_ball(self, ball: Ball) -> grSim_BallReplacement:
        ball_replacement = grSim_BallReplacement()
        ball_replacement.x = ball.x
        ball_replacement.y = ball.y
        ball_replacement.vx = ball.v_x
        ball_replacement.vy = ball.v_y
        return ball_replacement

    def _to_grsim_replacement_robot(self, robot: Robot) -> grSim_RobotReplacement:
        robot_replacement = grSim_RobotReplacement()
        robot_replacement.x = robot.x
        robot_replacement.y = robot.y
        robot_replacement.dir = math.degrees(robot.orientation)
        robot_replacement.id = robot.id
        robot_replacement.yellowteam = robot.is_yellow
        robot_replacement.turnon = robot.turn_on
        return robot_replacement
