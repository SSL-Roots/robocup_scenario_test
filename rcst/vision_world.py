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
from typing import Dict

from .ball import Ball
from .robot import Robot

from .proto.ssl_vision_wrapper_pb2 import SSL_WrapperPacket
from .proto.ssl_vision_detection_pb2 import SSL_DetectionFrame
from .proto.ssl_vision_detection_pb2 import SSL_DetectionBall


class VisionWorld:
    def __init__(self):
        self._ball: List[Ball] = [Ball()]
        self._blue_robots: Dict[int, Robot] = {}
        self._yellow_robots: Dict[int, Robot] = {}

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

    def _update_with_detection_frame(self, detection: SSL_DetectionFrame) -> None:
        for ball in detection.balls:
            self._update_ball(ball)

    def _update_ball(self, ball: SSL_DetectionBall) -> None:
        # Convert mm to m
        self._ball = [Ball(x=ball.x * 0.001,
                           y=ball.y * 0.001,)]
