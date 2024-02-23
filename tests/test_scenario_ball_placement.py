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

import rcst.calc as calc
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

    rcst_comm.observer.reset()
    rcst_comm.change_referee_command('STOP', 3.0)

    rcst_comm.set_ball_placement_position(target_x, target_y)
    rcst_comm.change_referee_command('BALL_PLACEMENT_BLUE', 0.0)

    time.sleep(30)
    ball = rcst_comm.observer.get_world().get_ball()
    assert calc.distance(ball.x, ball.y, target_x, target_y) < 0.15
