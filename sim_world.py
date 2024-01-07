
from ball import Ball
from robot import Robot
import sys
from typing import List
from typing import Dict

sys.path.append("./proto/grsim")
from proto.grsim import grSim_Packet_pb2 as grsim_packet
from proto.grsim.grSim_Replacement_pb2 import grSim_Replacement
from proto.grsim.grSim_Replacement_pb2 import grSim_RobotReplacement
from proto.grsim.grSim_Replacement_pb2 import grSim_BallReplacement



class SimWorld:
    MAX_ROBOT_NUM = 11

    def __init__(self, field_length: float = 12.0, field_width: float = 9.0):
        self._ball: List[Ball] = []
        self._blue_robots: List[Robot] = []
        self._yellow_robots: List[Robot] = []
        self._field_length = field_length
        self._field_width = field_width

    @classmethod
    def make_empty_world(cls) -> 'SimWorld':
        """
        Make an empty world.
        All robots are turned off.
        Ball is placed at (0, 0).
        """
        empty_world = cls()
        empty_world._ball = [Ball()]
        empty_world._robots = empty_world._all_robots_turn_off()
        return empty_world

    def to_grsim_packet_string(self) -> bytes:
        """
        Convert this world to a grSim packet string.
        """
        packet = grsim_packet.grSim_Packet()
        packet.replacement.CopyFrom(self._to_grsim_replacement())
        return packet.SerializeToString()

    def set_ball(self, ball: Ball) -> None:
        self._ball = [ball]

    def _all_robots_turn_off(self) -> List[Robot]:
        OFFSET_X = 0.2
        OFFSET_Y = 0.2
        POS_Y = -self._field_width / 2.0 - 0.5
        robots = []
        for i in range(self.MAX_ROBOT_NUM):
            pos_x = i * OFFSET_X
            pos_y = POS_Y
            robots.append(Robot(id=i, turn_on=False, is_yellow=False, x=pos_x, y=pos_y))
            pos_y = POS_Y - OFFSET_Y
            robots.append(Robot(id=i, turn_on=False, is_yellow=True, x=pos_x, y=pos_y))
        return robots

    def _to_grsim_replacement(self) -> grSim_Replacement:
        replacement = grSim_Replacement()
        for robot in self._robots:
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
        robot_replacement.dir = robot.orientation
        robot_replacement.id = robot.id
        robot_replacement.yellowteam = robot.is_yellow
        robot_replacement.turnon = robot.turn_on
        return robot_replacement
