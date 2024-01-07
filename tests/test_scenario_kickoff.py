
import math
import time

from srssl.communication import Communication
from srssl.sim_world import SimWorld


def change_referee_command(comm: Communication, command: str, sleep_time: float):
    print("Change referee command to {}".format(command))
    comm.referee.set_command(command)
    time.sleep(sleep_time)


def test_kickoff_one_robot():
    comm = Communication()
    comm.start_thread()
    change_referee_command(comm, 'HALT', 0.1)

    world = SimWorld.make_empty_world()
    world.set_ball(0, 0)
    world.set_blue_robot(1, -0.5, 0.0, math.radians(0))
    comm.send_replacement(world)
    time.sleep(3)  # Wait for the robots to be placed.

    comm.observer.reset()
    change_referee_command(comm, 'STOP', 3)
    change_referee_command(comm, 'PREPARE_KICKOFF_BLUE', 3)
    change_referee_command(comm, 'NORMAL_START', 5)
    change_referee_command(comm, 'HALT', 0.1)

    comm.stop_thread()
    assert comm.observer.we_got_the_goal() is True
