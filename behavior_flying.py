from behavior import Behavior
import math
import pubsub.pub as pub

class Flying(Behavior):
    def __init__(self, speed, rotation_speed):
        super(Flying, self).__init__()
        self.speed = speed
        self.rotation_speed = rotation_speed

        pub.subscribe(self.key_w, "key-w")
        pub.subscribe(self.key_s, "key-s")
        pub.subscribe(self.key_a, "key-a")
        pub.subscribe(self.key_d, "key-d")
        pub.subscribe(self.rotate_y, "rotate-y")
        pub.subscribe(self.rotate_x, "rotate-x")

    def key_w(self):
        self.game_object.position[2] -= self.speed * math.cos(math.radians(self.game_object.y_rotation)) * math.cos(math.radians(-self.game_object.x_rotation))  # type: ignore
        self.game_object.position[0] += self.speed * math.sin(math.radians(self.game_object.y_rotation)) * math.cos(math.radians(-self.game_object.x_rotation))  # type: ignore
        self.game_object.position[1] += self.speed * math.sin(math.radians(-self.game_object.x_rotation))  # type: ignore
        self.game_object._moved = True  # type: ignore

    def key_s(self):
        self.game_object.position[2] += self.speed * math.cos(math.radians(self.game_object.y_rotation)) * math.cos(math.radians(-self.game_object.x_rotation))  # type: ignore
        self.game_object.position[0] -= self.speed * math.sin(math.radians(self.game_object.y_rotation)) * math.cos(math.radians(-self.game_object.x_rotation))  # type: ignore
        self.game_object.position[1] -= self.speed * math.sin(math.radians(-self.game_object.x_rotation))  # type: ignore
        self.game_object._moved = True  # type: ignore

    def key_a(self):
        self.game_object.position[2] -= self.speed * math.cos(math.radians(self.game_object.y_rotation - 90))  # type: ignore
        self.game_object.position[0] += self.speed * math.sin(math.radians(self.game_object.y_rotation - 90))  # type: ignore
        self.game_object._moved = True  # type: ignore

    def key_d(self):
        self.game_object.position[2] -= self.speed * math.cos(math.radians(self.game_object.y_rotation + 90))  # type: ignore
        self.game_object.position[0] += self.speed * math.sin(math.radians(self.game_object.y_rotation + 90))  # type: ignore
        self.game_object._moved = True  # type: ignore

    def rotate_y(self, amount):
        self.game_object.y_rotation += amount * self.rotation_speed  # type: ignore

    def rotate_x(self, amount):
        self.game_object.x_rotation += amount * self.rotation_speed  # type: ignore
