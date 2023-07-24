from game_object import GameObject
from pubsub import pub
import math
import numpy as np


class Player(GameObject):
    def __init__(self, kind, id, position, size):
        super(Player, self).__init__(kind, id, position, size)

        self.collisions = []

        pub.subscribe(self.key_w, "key-w")
        pub.subscribe(self.key_s, "key-s")
        pub.subscribe(self.key_a, "key-a")
        pub.subscribe(self.key_d, "key-d")
        pub.subscribe(self.rotate_y, "rotate-y")
        pub.subscribe(self.rotate_x, "rotate-x")

    def key_w(self):
        self.position[2] -= 0.1 * math.cos(math.radians(self.y_rotation))
        self.position[0] += 0.1 * math.sin(math.radians(self.y_rotation))
        self._moved = True

    def key_s(self):
        self.position[2] += 0.1 * math.cos(math.radians(self.y_rotation))
        self.position[0] -= 0.1 * math.sin(math.radians(self.y_rotation))
        self._moved = True

    def key_a(self):
        self.position[2] -= 0.1 * math.cos(math.radians(self.y_rotation - 90))
        self.position[0] += 0.1 * math.sin(math.radians(self.y_rotation - 90))
        self._moved = True

    def key_d(self):
        self.position[2] -= 0.1 * math.cos(math.radians(self.y_rotation + 90))
        self.position[0] += 0.1 * math.sin(math.radians(self.y_rotation + 90))
        self._moved = True

    def rotate_y(self, amount):
        self.y_rotation += amount

    def rotate_x(self, amount):
        self.x_rotation += amount

    def tick(self):
        # Handle collisions
        if self.collisions:
            mypos = np.array(self.position)

            for other in self.collisions:
                otherpos = np.array(other.position)
                distance = np.linalg.norm(mypos - otherpos)
                direction_vector = (mypos - otherpos) / distance
                self.position = otherpos + (distance + 0.1) * direction_vector

        self.collisions = []
        self._moved = False
