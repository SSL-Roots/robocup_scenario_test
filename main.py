#!/usr/bin/env python3
# coding: UTF-8

from grsim_replacement import GrSimReplacement
from sim_world import SimWorld


if __name__ == '__main__':
    sender = GrSimReplacement('localhost', 20011)

    world = SimWorld.make_empty_world()

    sender.send(world.to_grsim_packet_string())
