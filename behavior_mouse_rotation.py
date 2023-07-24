from behavior import Behavior
import math
import pubsub.pub as pub


class MouseRotation(Behavior):
    def __init__(self, speed):
        super(MouseRotation, self).__init__()
        self.speed = speed

        pub.subscribe(self.rotate_y, "rotate-y")
        pub.subscribe(self.rotate_x, "rotate-x")

    def rotate_y(self, amount):
        self.game_object.y_rotation += amount * self.speed # type: ignore

    def rotate_x(self, amount):
        self.game_object.x_rotation += amount * self.speed # type: ignore