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

from .ball import Ball
from .robot import Robot
from .robot import RobotDict

from .proto.ssl_vision_detection_pb2 import SSL_DetectionBall
from .proto.ssl_vision_detection_pb2 import SSL_DetectionFrame
from .proto.ssl_vision_detection_pb2 import SSL_DetectionRobot
from .proto.ssl_vision_wrapper_pb2 import SSL_WrapperPacket


class VisionWorld:
    def __init__(self):
        self._ball: List[Ball] = [Ball()]
        self._blue_robots: RobotDict = {}
        self._yellow_robots: RobotDict = {}
        self._timestamp: float = 0.0

    def update_with_vision_packet(self, data: bytes) -> None:
        packet = SSL_WrapperPacket()
        try:
            packet.ParseFromString(data)
        except Exception as e:
            print("Failed to parse vision packet. Details: {}".format(e))
            return

        if packet.HasField("detection"):
            self._update_with_detection_frame(packet.detection)

    def get_ball(self) -> Ball:
        return self._ball[0]

    def get_blue_robots(self) -> RobotDict:
        return self._blue_robots

    def get_yellow_robots(self) -> RobotDict:
        return self._yellow_robots

    def get_timestamp(self) -> float:
        return self._timestamp

    def _update_with_detection_frame(self, detection: SSL_DetectionFrame) -> None:
        for ball in detection.balls:
            self._update_ball(ball)

        self._update_blue_robots(detection.robots_blue)
        self._update_yellow_robots(detection.robots_yellow)

        if detection.t_capture > self._timestamp:
            self._timestamp = detection.t_capture

    def _update_ball(self, ball: SSL_DetectionBall) -> None:
        # Convert mm to m
        self._ball = [Ball(x=ball.x * 0.001,
                           y=ball.y * 0.001,)]

    def _update_blue_robots(self, robots: List[SSL_DetectionRobot]) -> None:
        for robot in robots:
            self._blue_robots[robot.robot_id] = Robot(x=robot.x * 0.001,
                                                      y=robot.y * 0.001,
                                                      orientation=robot.orientation,
                                                      id=robot.robot_id,
                                                      is_yellow=False)

    def _update_yellow_robots(self, robots: List[SSL_DetectionRobot]) -> None:
        for robot in robots:
            self._yellow_robots[robot.robot_id] = Robot(x=robot.x * 0.001,
                                                        y=robot.y * 0.001,
                                                        orientation=robot.orientation,
                                                        id=robot.robot_id,
                                                        is_yellow=True)
