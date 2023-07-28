from behavior import Behavior
import math
import pubsub.pub as pub
import numpy


class KeyFly(Behavior):
    def __init__(self, speed):
        super(KeyFly, self).__init__()
        self.speed = speed

        pub.subscribe(self.key_w, "key-w")
        pub.subscribe(self.key_s, "key-s")
        pub.subscribe(self.key_a, "key-a")
        pub.subscribe(self.key_d, "key-d")

    def key_w(self, camera_direction):
        camera_direction = numpy.array(camera_direction)
        current = numpy.array(self.game_object.position)  # type: ignore
        position = (current + camera_direction * self.speed).tolist()
        self.game_object.position = position  # type: ignore
        self.game_object._moved = True  # type: ignore

    def key_s(self, camera_direction):
        camera_direction = numpy.array(camera_direction)
        current = numpy.array(self.game_object.position)  # type: ignore
        position = (current - camera_direction * self.speed).tolist()  # type: ignore
        self.game_object.position = position  # type: ignore
        self.game_object._moved = True  # type: ignore

    def key_a(self):
        self.game_object.position[2] -= self.speed * math.cos(math.radians(self.game_object.y_rotation - 90))  # type: ignore
        self.game_object.position[0] += self.speed * math.sin(math.radians(self.game_object.y_rotation - 90))  # type: ignore
        self.game_object._moved = True  # type: ignore

    def key_d(self):
        self.game_object.position[2] -= self.speed * math.cos(math.radians(self.game_object.y_rotation + 90))  # type: ignore
        self.game_object.position[0] += self.speed * math.sin(math.radians(self.game_object.y_rotation + 90))  # type: ignore
        self.game_object._moved = True  # type: ignore
