
import math
import time

from rcst.sim_world import SimWorld


def test_our_kickoff(rcst_comm):
    world = SimWorld.make_empty_world()
    world.set_ball(0, 0)
    world.set_blue_robot(1, -0.5, 0.0, math.radians(0))
    rcst_comm.send_replacement(world)
    time.sleep(3)  # Wait for the robots to be placed.

    rcst_comm.observer.reset()
    rcst_comm.change_referee_command('STOP', 3.0)
    rcst_comm.change_referee_command('PREPARE_KICKOFF_BLUE', 3.0)
    rcst_comm.change_referee_command('NORMAL_START', 5.0)

    assert rcst_comm.observer.ball_has_been_in_positive_goal() is True


def test_their_kickoff(rcst_comm):
    world = SimWorld.make_empty_world()
    world.set_ball(0, 0)
    world.set_blue_robot(0, -5.5, 0.0, math.radians(0))
    world.set_yellow_robot(0, 0.1, 0.0, math.radians(180))
    rcst_comm.send_replacement(world)
    time.sleep(3)  # Wait for the robots to be placed.

    rcst_comm.observer.reset()
    rcst_comm.change_referee_command('STOP', 3.0)
    rcst_comm.change_referee_command('PREPARE_KICKOFF_YELLOW', 3.0)
    rcst_comm.change_referee_command('NORMAL_START', 1.0)

    # Shoot to our goal.
    world = SimWorld()
    world.set_ball(0, 0, -6.0, 0.5)
    rcst_comm.send_replacement(world)
    time.sleep(5)

    assert rcst_comm.observer.ball_has_been_in_negative_goal() is False
