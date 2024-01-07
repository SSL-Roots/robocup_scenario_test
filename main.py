#!/usr/bin/env python3
# coding: UTF-8

from grsim_replacement import GrSimReplacement
from sim_world import SimWorld
import math


if __name__ == '__main__':
    sender = GrSimReplacement('localhost', 20011)

    world = SimWorld.make_empty_world()

    world.set_ball(0.0, -0.0, 7.0, 5.0)
    world.set_robot(0, False, 0.0, 0.0, 0.0)
    world.set_robot(1, True, 1.0, -2.0, math.radians(-90.0))

    sender.send(world.to_grsim_packet_string())
