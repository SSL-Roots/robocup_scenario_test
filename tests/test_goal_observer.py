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

from rcst.observer.goal_observer import GoalObserver
from rcst.ball import Ball


def test_ball_has_been_in_goal():
    goal = GoalObserver(field_half_length=6.0, goal_half_width=0.9, goal_depth=0.18)

    # ----- Test positive side -----
    goal.update(Ball(x=6.0, y=0.9))
    assert goal.ball_has_been_in_positive_goal() is False
    assert goal.ball_has_been_in_negative_goal() is False

    goal.update(Ball(x=6.18, y=-0.9))
    assert goal.ball_has_been_in_positive_goal() is False
    assert goal.ball_has_been_in_negative_goal() is False

    goal.update(Ball(x=6.01, y=0.89))
    assert goal.ball_has_been_in_positive_goal() is True
    assert goal.ball_has_been_in_negative_goal() is False

    # ----- Test reset() -----
    goal.reset()
    assert goal.ball_has_been_in_positive_goal() is False
    assert goal.ball_has_been_in_negative_goal() is False

    goal.update(Ball(x=6.17, y=-0.89))
    assert goal.ball_has_been_in_positive_goal() is True
    assert goal.ball_has_been_in_negative_goal() is False

    # ----- Test negative side -----
    goal.reset()
    goal.update(Ball(x=-6.01, y=0.89))
    assert goal.ball_has_been_in_positive_goal() is False
    assert goal.ball_has_been_in_negative_goal() is True

    # ----- Test reset() -----
    goal.reset()
    assert goal.ball_has_been_in_positive_goal() is False
    assert goal.ball_has_been_in_negative_goal() is False

    goal.update(Ball(x=-6.17, y=-0.89))
    assert goal.ball_has_been_in_positive_goal() is False
    assert goal.ball_has_been_in_negative_goal() is True
