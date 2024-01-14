
import math
import time

from rcst.sim_world import SimWorld


def test_our_kickoff(comm, change_referee_command):
    change_referee_command('HALT', 0.1)

    world = SimWorld.make_empty_world()
    world.set_ball(0, 0)
    world.set_blue_robot(1, -0.5, 0.0, math.radians(0))
    comm.send_replacement(world)
    time.sleep(3)  # Wait for the robots to be placed.

    comm.observer.reset()
    change_referee_command('STOP', 3)
    change_referee_command('PREPARE_KICKOFF_BLUE', 3)
    change_referee_command('NORMAL_START', 5)
    change_referee_command('HALT', 0.1)

    assert comm.observer.ball_has_been_in_positive_goal() is True


def test_their_kickoff(comm, change_referee_command):
    change_referee_command('HALT', 0.1)

    world = SimWorld.make_empty_world()
    world.set_ball(0, 0)
    world.set_blue_robot(0, -5.5, 0.0, math.radians(0))
    world.set_yellow_robot(0, 0.1, 0.0, math.radians(180))
    comm.send_replacement(world)
    time.sleep(3)  # Wait for the robots to be placed.

    comm.observer.reset()
    change_referee_command('STOP', 3)
    change_referee_command('PREPARE_KICKOFF_YELLOW', 3)
    change_referee_command('NORMAL_START', 1)

    # Shoot to our goal.
    world = SimWorld()
    world.set_ball(0, 0, -6.0, 0.5)
    comm.send_replacement(world)
    time.sleep(5)

    change_referee_command('HALT', 0.1)

    assert comm.observer.ball_has_been_in_negative_goal() is False
