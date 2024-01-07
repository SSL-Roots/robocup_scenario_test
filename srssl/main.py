#!/usr/bin/env python3
# coding: UTF-8

from grsim_replacement import GrSimReplacement
from referee_sender import RefereeSender
from sim_referee import SimReferee
from sim_world import SimWorld
from vision_receiver import VisionReceiver
from vision_world import VisionWorld
from world_observer import WorldObserver

import math
import time

def set_sim_world():
    sender = GrSimReplacement('localhost', 20011)

    world = SimWorld.make_empty_world()

    world.set_ball(0.0, -0.0, 7.0, 5.0)
    world.set_robot(0, False, 0.0, 0.0, 0.0)
    world.set_robot(1, True, 1.0, -2.0, math.radians(-90.0))

    sender.send(world.to_grsim_packet_string())

def observe_goal():
    receiver = VisionReceiver('224.5.23.2', 10006)
    vision_world = VisionWorld()
    observer = WorldObserver()

    start_time = time.time()
    while (time.time() - start_time) < 5.0:
        data = receiver.receive()
        if data is not None:
            vision_world.update_with_vision_packet(data)
            observer.update(vision_world)
            print("we_got_the_goal: {}".format(observer.we_got_the_goal()))


if __name__ == '__main__':
    sender = RefereeSender('224.5.23.1', 10003)
    referee = SimReferee()

    referee.set_command("HALT")
    sender.send(referee.to_referee_packet_string())
