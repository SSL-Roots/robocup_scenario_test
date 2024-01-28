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

import socket


class RefereeSender:
    def __init__(self, addr, port):
        self._addr = addr
        self._port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Configure multicast TTL
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    def send(self, msg: bytes):
        try:
            self.sock.sendto(msg, (self._addr, self._port))
        except Exception as e:
            print("Failed to send referee message. Details: {}".format(e))
