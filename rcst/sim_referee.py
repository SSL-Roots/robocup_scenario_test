
import time

from .proto.referee.ssl_gc_referee_message_pb2 import Referee


class SimReferee:
    def __init__(self):
        self._stage = Referee.NORMAL_FIRST_HALF_PRE
        self._command = Referee.HALT
        self._command_counter = 0
        self._command_timestamp = self._get_time_stamp_us()

    def set_command(self, command: str) -> bool:
        if not hasattr(Referee, command):
            print("Invalid command: {}".format(command))
            return False
        self._command = getattr(Referee, command)
        self._command_counter += 1
        self._command_timestamp = self._get_time_stamp_us()

    def to_referee_packet_string(self) -> bytes:
        packet = Referee()
        packet.packet_timestamp = self._get_time_stamp_us()
        packet.stage = self._stage
        packet.command = self._command
        packet.command_counter = self._command_counter
        packet.command_timestamp = self._command_timestamp
        packet.yellow.CopyFrom(self._make_team_info("Yellow"))
        packet.blue.CopyFrom(self._make_team_info("Blue"))
        return packet.SerializeToString()

    def _get_time_stamp_us(self) -> int:
        return time.time_ns() // 1000

    def _make_team_info(self, name: str) -> Referee.TeamInfo:
        team_info = Referee.TeamInfo()
        team_info.name = name
        team_info.score = 0
        team_info.red_cards = 0
        team_info.yellow_cards = 0
        team_info.timeouts = 0
        team_info.timeout_time = 0
        team_info.goalkeeper = 0
        team_info.max_allowed_bots = 11
        return team_info
