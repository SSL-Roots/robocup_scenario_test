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

import time


def test_our_ball_placement(rcst_comm):
    rcst_comm.send_empty_world()
    rcst_comm.send_ball(0, 0)
    rcst_comm.send_blue_robot(1, -0.5, 0.0, 0.0)
    rcst_comm.send_blue_robot(2, -1.0, 0.0, 0.0)
    rcst_comm.send_blue_robot(3, -1.5, 0.0, 0.0)
    rcst_comm.send_blue_robot(4, -2.0, 0.0, 0.0)
    time.sleep(1)  # Wait for the robots to be placed.

    target_x = 1.0
    target_y = 1.0

    rcst_comm.observer.ball_placement().set_targets(
        target_x, target_y, for_blue_team=True)

    rcst_comm.change_referee_command('STOP', 3.0)

    rcst_comm.set_ball_placement_position(target_x, target_y)
    rcst_comm.change_referee_command('BALL_PLACEMENT_BLUE', 0.0)

    placement_success = False
    for _ in range(30):
        if rcst_comm.observer.ball_placement().success():
            placement_success = True
            break
        time.sleep(1)
    assert placement_success is True
