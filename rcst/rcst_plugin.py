
import pytest
from rcst.communication import Communication


@pytest.fixture
def rcst_comm():
    comm_instance = Communication()
    comm_instance.start_thread()

    yield comm_instance

    comm_instance.stop_thread()
