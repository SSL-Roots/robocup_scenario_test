
import pytest
from rcst.communication import Communication


@pytest.fixture
def rcst_comm():
    comm_instance = Communication()
    comm_instance.start_thread()
    comm_instance.change_referee_command('HALT', 0.1)

    yield comm_instance

    comm_instance.change_referee_command('HALT', 0.1)
    comm_instance.stop_thread()
