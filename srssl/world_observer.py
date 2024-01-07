
from .ball import Ball
from .vision_world import VisionWorld


class WorldObserver:
    """
    Observes the world and updates the state of the world.

    Our side is the negative side of the x-axis.
    """
    def __init__(self, field_length: float = 12.0, field_width: float = 9.0,
                 goal_width: float = 1.8, goal_depth: float = 0.18):
        self._field_length = field_length
        self._field_half_length = field_length / 2.0
        self._field_width = field_width
        self._goal_width = goal_width
        self._goal_half_width = goal_width / 2.0
        self._goal_depth = goal_depth

        self._we_got_the_goal = False

    def reset(self) -> None:
        self._our_goal = False

    def we_got_the_goal(self) -> bool:
        return self._we_got_the_goal

    def update(self, vision_world: VisionWorld) -> None:

        # Check if the ball is in their goal.
        if not self._we_got_the_goal:
            self._we_got_the_goal = self._check_ball_in_their_goal(vision_world.get_ball())

    def _check_ball_in_their_goal(self, ball: Ball) -> bool:
        in_goal_depth = ball.x > self._field_half_length \
                        and ball.x < self._field_half_length + self._goal_depth
        in_goal_width = abs(ball.y) < self._goal_half_width
        return in_goal_depth and in_goal_width
