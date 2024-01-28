
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
    parser.addoption("--grsim_addr", action="store", default="127.0.0.1",
                     help="grSim address")
    parser.addoption("--grsim_port", action="store", default="20011",
                     help="grSim port")


@pytest.fixture
def rcst_config(request):
    return {
        "vision_addr": request.config.getoption("--vision_addr"),
        "vision_port": int(request.config.getoption("--vision_port")),
        "referee_addr": request.config.getoption("--referee_addr"),
        "referee_port": int(request.config.getoption("--referee_port")),
        "grsim_addr": request.config.getoption("--grsim_addr"),
        "grsim_port": int(request.config.getoption("--grsim_port"))
    }


@pytest.fixture
def rcst_comm(rcst_config):
    comm_instance = Communication(
        vision_addr=rcst_config["vision_addr"],
        vision_port=rcst_config["vision_port"],
        referee_addr=rcst_config["referee_addr"],
        referee_port=rcst_config["referee_port"],
        grsim_addr=rcst_config["grsim_addr"],
        grsim_port=rcst_config["grsim_port"]
    )
    comm_instance.start_thread()
    comm_instance.change_referee_command('HALT', 0.1)

    yield comm_instance

    comm_instance.change_referee_command('HALT', 0.1)
    comm_instance.stop_thread()
