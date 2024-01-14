
from rcst.ball import Ball
from rcst.vision_world import VisionWorld
from rcst.world_observer import WorldObserver


def test_ball_has_been_in_goal():
    observer = WorldObserver()
    vision_world = VisionWorld()

    vision_world._ball = [Ball(x=0.0, y=0.0)]
    observer.update(vision_world)
    assert observer.ball_has_been_in_positive_goal() is False
    assert observer.ball_has_been_in_negative_goal() is False

    vision_world._ball = [Ball(x=6.01, y=0.0)]
    observer.update(vision_world)
    assert observer.ball_has_been_in_positive_goal() is True
    assert observer.ball_has_been_in_negative_goal() is False

    observer.reset()
    assert observer.ball_has_been_in_positive_goal() is False
    assert observer.ball_has_been_in_negative_goal() is False

    vision_world._ball = [Ball(x=-6.01, y=0.0)]
    observer.update(vision_world)
    assert observer.ball_has_been_in_positive_goal() is False
    assert observer.ball_has_been_in_negative_goal() is True
