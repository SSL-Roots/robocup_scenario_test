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

import threading
import time

from .grsim_replacement import GrSimReplacement
from .referee_sender import RefereeSender
from .sim_referee import SimReferee
from .sim_sender import SimSender
from .sim_world import SimWorld
from .vision_receiver import VisionReceiver
from .vision_world import VisionWorld
from .world_observer import WorldObserver


class Communication:
    def __init__(self,
                 vision_addr: str = '224.5.23.2', vision_port: int = 10006,
                 referee_addr: str = '224.5.23.1', referee_port: int = 10003,
                 grsim_addr: str = 'localhost', grsim_port: int = 20011,
                 sim_addr: str = 'localhost', sim_port: int = 10300
                 ):
        self.observer = WorldObserver()
        self.referee = SimReferee()

        self._receiver = VisionReceiver(vision_addr, vision_port)
        self._ref_sender = RefereeSender(referee_addr, referee_port)
        self._grsim_replacement = GrSimReplacement(grsim_addr, grsim_port)
        self._sim_sender = SimSender(sim_addr, sim_port)
        self._vision_thread = threading.Thread(target=self._vision_update)
        self._referee_thread = threading.Thread(target=self._referee_update)

        self._thread_running = True

    def send_replacement(self, world: SimWorld):
        self._grsim_replacement.send(world.to_grsim_packet_string())

    def send_simulator_command(self, world: SimWorld):
        self._sim_sender.send(world.to_sim_command_packet_string())

    def start_thread(self):
        self._thread_running = True
        self._vision_thread.start()
        self._referee_thread.start()

    def stop_thread(self):
        self._thread_running = False
        self._vision_thread.join()
        self._referee_thread.join()

    def change_referee_command(self, command: str, sleep_time: float):
        print("Change referee command to {}, and wait {} seconds.".format(command, sleep_time))
        self.referee.set_command(command)
        time.sleep(sleep_time)

    def send_empty_world(self, sleep_time: float = 0.1):
        print("Send empty world.")
        world = SimWorld.make_empty_world()
        self.send_simulator_command(world)
        time.sleep(sleep_time)

    def send_ball(self, x: float, y: float, v_x: float = 0.0, v_y: float = 0.0,
                  sleep_time: float = 0.1):
        print("Send ball at ({}, {}) with velocity ({}, {}).".format(x, y, v_x, v_y))
        world = SimWorld()
        world.set_ball(x, y, v_x, v_y)
        self.send_simulator_command(world)
        time.sleep(sleep_time)

    def send_blue_robot(self, robot_id: int, x: float, y: float, orientation: float,
                        sleep_time: float = 0.1):
        print("Send blue robot {} at ({}, {}) with orientation {}.".format(
            robot_id, x, y, orientation))
        world = SimWorld()
        world.set_blue_robot(robot_id, x, y, orientation)
        self.send_replacement(world)
        time.sleep(sleep_time)

    def send_yellow_robot(self, robot_id: int, x: float, y: float, orientation: float,
                          sleep_time: float = 0.1):
        print("Send yellow robot {} at ({}, {}) with orientation {}.".format(
            robot_id, x, y, orientation))
        world = SimWorld()
        world.set_yellow_robot(robot_id, x, y, orientation)
        self.send_replacement(world)
        time.sleep(sleep_time)

    def _vision_update(self):
        vision_world = VisionWorld()
        while self._thread_running:
            data = self._receiver.receive()
            if data is not None:
                vision_world.update_with_vision_packet(data)
                self.observer.update(vision_world)

    def _referee_update(self):
        while self._thread_running:
            self._ref_sender.send(self.referee.to_referee_packet_string())
            time.sleep(0.1)
