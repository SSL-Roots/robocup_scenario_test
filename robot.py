
from typing import List

class Robot:
    def __init__(self, x: float = 0.0, y: float = 0.0, orientation: float = 0.0,
                 is_yellow: bool = False, id: int = 0, turn_on: bool = True) -> None:
        self.x = x
        self.y = y
        self.orientation = orientation
        self.is_yellow = is_yellow
        self.id = id
        self.turn_on = turn_on

        self._v_x: List[float] = []
        self._v_y: List[float] = []
        self._v_angular: List[float] = []
        self._kick_speed_x: List[float] = []
        self._kick_speed_z: List[float] = []
        self._dribble: List[bool] = []

    def set_command(self, v_x: float, v_y: float, v_angular: float,
                    kick_speed_x: float, kick_speed_z, dribble: bool) -> None:
        self._v_x = [v_x]
        self._v_y = [v_y]
        self._v_angular = [v_angular]
        self._kick_speed_x = [kick_speed_x]
        self._kick_speed_z = [kick_speed_z]
        self._dribble = [dribble]

    def has_command(self) -> bool:
        return len(self._v_x) and len(self._v_y) and len(self._v_angular) \
               and len(self._kick_speed_x) and len(self._kick_speed_z) and len(self._dribble)
