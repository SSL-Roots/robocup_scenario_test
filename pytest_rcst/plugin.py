
import pytest
import time

from rcst.communication import Communication


def pytest_addoption(parser):
    parser.addoption("--vision-port", action="store", default=10006, type=int)


@pytest.fixture
def comm(request):
    vision_port = request.config.getoption("--vision-port")
    comm = Communication(vision_port=vision_port)
    comm.start_thread()
    yield comm
    comm.stop_thread()


@pytest.fixture
def change_referee_command(comm):
    def _change_referee_command(command: str, sleep_time: float):
        print("Change referee command to {}".format(command))
        comm.referee.set_command(command)
        time.sleep(sleep_time)
    return _change_referee_command
