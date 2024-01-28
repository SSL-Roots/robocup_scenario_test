
import threading
import time

from .grsim_replacement import GrSimReplacement
from .referee_sender import RefereeSender
from .sim_referee import SimReferee
from .sim_world import SimWorld
from .vision_receiver import VisionReceiver
from .vision_world import VisionWorld
from .world_observer import WorldObserver


class Communication:
    def __init__(self,
                 vision_addr: str = '224.5.23.2', vision_port: int = 10006,
                 referee_addr: str = '224.5.23.1', referee_port: int = 10003,
                 grsim_addr: str = 'localhost', grsim_port: int = 20011,
                 ):
        self.observer = WorldObserver()
        self.referee = SimReferee()

        self._receiver = VisionReceiver(vision_addr, vision_port)
        self._ref_sender = RefereeSender(referee_addr, referee_port)
        self._grsim_replacement = GrSimReplacement(grsim_addr, grsim_port)
        self._vision_thread = threading.Thread(target=self._vision_update)
        self._referee_thread = threading.Thread(target=self._referee_update)

        self._thread_running = True

    def send_replacement(self, world: SimWorld):
        self._grsim_replacement.send(world.to_grsim_packet_string())

    def start_thread(self):
        self._thread_running = True
        self._vision_thread.start()
        self._referee_thread.start()

    def stop_thread(self):
        self._thread_running = False
        self._vision_thread.join()
        self._referee_thread.join()

    def change_referee_command(self, command: str, sleep_time: float):
        print("Change referee command to {}, and wait {} seconds.".format(command, sleep_time))
        self.referee.set_command(command)
        time.sleep(sleep_time)

    def _vision_update(self):
        vision_world = VisionWorld()
        while self._thread_running:
            data = self._receiver.receive()
            if data is not None:
                vision_world.update_with_vision_packet(data)
                self.observer.update(vision_world)

    def _referee_update(self):
        while self._thread_running:
            self._ref_sender.send(self.referee.to_referee_packet_string())
            time.sleep(0.1)
