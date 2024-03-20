# Copyright 2024 Roots
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..ball import Ball
from ..robot import RobotDict
from typing import Callable


class CustomizedObserver:
    """
    Observes what you want to observe
    """
    def __init__(self):
        self._sticky_true_callbacks: dict[str, Callable[[Ball, RobotDict, RobotDict], bool]] = {}
        self._is_true_sticky: dict[str, bool] = {}

    def update(self, ball: Ball, blue_robots: RobotDict, yellow_robots: RobotDict) -> None:
        for name, callback in self._sticky_true_callbacks.items():
            if not self._is_true_sticky[name]:
                self._is_true_sticky[name] = callback(ball, blue_robots, yellow_robots)

    def reset_results(self) -> None:
        for name in self._is_true_sticky:
            self._is_true_sticky[name] = False

    def register_sticky_true_callback(
            self, name: str, callback: Callable[[Ball, RobotDict, RobotDict], bool]) -> None:
        self._sticky_true_callbacks[name] = callback
        self._is_true_sticky[name] = False

    def get_result(self, name: str) -> bool:
        if name not in self._is_true_sticky:
            raise ValueError(f"Callback {name} not registered")

        return self._is_true_sticky[name]
