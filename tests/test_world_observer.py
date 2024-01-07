
from srssl.ball import Ball
from srssl.vision_world import VisionWorld
from srssl.world_observer import WorldObserver


def test_we_got_the_ball():
    observer = WorldObserver()
    vision_world = VisionWorld()

    vision_world._ball = [Ball(x=0.0, y=0.0)]
    observer.update(vision_world)
    assert observer.we_got_the_ball() is False

    vision_world._ball = [Ball(x=6.01, y=0.0)]
    observer.update(vision_world)
    assert observer.we_got_the_ball() is True
