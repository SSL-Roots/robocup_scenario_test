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

import pytest
from rcst.communication import Communication


def pytest_addoption(parser):
    parser.addoption("--vision_addr", action="store", default="224.5.23.2",
                     help="Vision multicast address")
    parser.addoption("--vision_port", action="store", default="10006",
                     help="Vision multicast port")
    parser.addoption("--referee_addr", action="store", default="224.5.23.1",
                     help="Referee multicast address")
    parser.addoption("--referee_port", action="store", default="10003",
                     help="Referee multicast port")
    parser.addoption("--sim_addr", action="store", default="127.0.0.1",
                     help="Simulator address")
    parser.addoption("--sim_port", action="store", default="10300",
                     help="Simulator port")


@pytest.fixture
def rcst_config(request):
    return {
        "vision_addr": request.config.getoption("--vision_addr"),
        "vision_port": int(request.config.getoption("--vision_port")),
        "referee_addr": request.config.getoption("--referee_addr"),
        "referee_port": int(request.config.getoption("--referee_port")),
        "sim_addr": request.config.getoption("--sim_addr"),
        "sim_port": int(request.config.getoption("--sim_port"))
    }


@pytest.fixture
def rcst_comm(rcst_config):
    comm_instance = Communication(
        vision_addr=rcst_config["vision_addr"],
        vision_port=rcst_config["vision_port"],
        referee_addr=rcst_config["referee_addr"],
        referee_port=rcst_config["referee_port"],
        sim_addr=rcst_config["sim_addr"],
        sim_port=rcst_config["sim_port"]
    )
    comm_instance.start_thread()
    comm_instance.change_referee_command('HALT', 0.1)

    yield comm_instance

    comm_instance.change_referee_command('HALT', 0.1)
    comm_instance.stop_thread()
