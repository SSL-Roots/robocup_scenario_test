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

from rcst.ball import Ball
from rcst.vision_world import VisionWorld
from rcst.world_observer import WorldObserver


def test_goal_instance():
    # Note: The goal observer's tests are already covered in the test_goal_observer.py file.
    observer = WorldObserver(
        field_length=12.0, field_width=9.0, goal_width=1.8, goal_depth=0.18)

    vision_world = VisionWorld()
    vision_world._ball = [Ball(x=6.01, y=0.0)]
    observer.update(vision_world)

    assert observer.goal().ball_has_been_in_positive_goal() is True
