
import math
import threading
import time

from srssl.sim_world import SimWorld

from srssl.grsim_replacement import GrSimReplacement

from srssl.referee_sender import RefereeSender
from srssl.sim_referee import SimReferee
from srssl.vision_receiver import VisionReceiver
from srssl.vision_world import VisionWorld
from srssl.world_observer import WorldObserver


class Comm:
    def __init__(self):
        self.observer = WorldObserver()
        self.referee = SimReferee()

        self._receiver = VisionReceiver('224.5.23.2', 10006)
        self._ref_sender = RefereeSender('224.5.23.1', 10003)
        self._vision_thread = threading.Thread(target=self._vision_update)
        self._referee_thread = threading.Thread(target=self._referee_update)

        self._running = True

    def start(self):
        self._running = True
        self._vision_thread.start()
        self._referee_thread.start()

    def stop(self):
        self._running = False
        self._vision_thread.join()
        self._referee_thread.join()

    def _vision_update(self):
        vision_world = VisionWorld()
        while self._running:
            data = self._receiver.receive()
            if data is not None:
                vision_world.update_with_vision_packet(data)
                self.observer.update(vision_world)

    def _referee_update(self):
        while self._running:
            self._ref_sender.send(self.referee.to_referee_packet_string())
            time.sleep(0.1)


def change_referee_command(comm: Comm, command: str, sleep_time: float):
    print("Change referee command to {}".format(command))
    comm.referee.set_command(command)
    time.sleep(sleep_time)


def test_kickoff_one_robot():
    comm = Comm()
    comm.start()
    change_referee_command(comm, 'HALT', 0.1)

    grsim = GrSimReplacement('localhost', 20011)

    world = SimWorld.make_empty_world()
    world.set_ball(0, 0)
    world.set_robot(1, False, -0.5, 0.0, math.radians(0))
    grsim.send(world.to_grsim_packet_string())
    time.sleep(5)  # Wait for the robots to be placed.

    comm.observer.reset()
    change_referee_command(comm, 'STOP', 3)
    change_referee_command(comm, 'PREPARE_KICKOFF_BLUE', 3)
    change_referee_command(comm, 'NORMAL_START', 5)
    change_referee_command(comm, 'HALT', 0.1)

    comm.stop()
    assert comm.observer.we_got_the_goal() is True
