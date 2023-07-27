from behavior import Behavior
from game_logic import GameLogic
import numpy as np


class Platform(Behavior):
    def __init__(self, finish, speed, transport):
        super(Platform, self).__init__()

        self.start = None
        self.finish = np.array(finish)
        self.speed = speed
        self.transport = transport

    def connect(self, game_object):
        super(Platform, self).connect(game_object)
        self.start = np.array(self.game_object.position)  # type: ignore
        self.distance = np.linalg.norm(self.finish - self.start)
        self.direction_vector = (self.finish - self.start) / self.distance

    def tick(self):
        current = np.array(self.game_object.position)  # type: ignore
        distance = np.linalg.norm(current - self.start)

        riders = []
        if self.transport:
            self.game_object.position[1] += 0.1  # type: ignore

            for other in GameLogic.game_objects:
                if not GameLogic.collide(
                    self.game_object, GameLogic.game_objects[other]
                ):
                    continue

                if GameLogic.game_objects[other] in self.game_object.collisions:  # type: ignore
                    continue

                riders.append(GameLogic.game_objects[other])

            self.game_object.position[1] -= 0.1  # type: ignore

        already_moved = set()
        if distance >= self.distance:
            self.direction_vector = (
                -(1 / np.linalg.norm(self.direction_vector)) * self.direction_vector
            )
            self.game_object.position = (self.finish).tolist()  # type: ignore
            temp = self.start
            self.start = self.finish
            self.finish = temp
        else:
            self.game_object.position = (self.start + (distance + self.speed) * self.direction_vector).tolist()  # type: ignore
            self.move_riders(riders, self.direction_vector, self.speed, already_moved)

        self.game_object._moved = True  # type: ignore

    def move_riders(self, riders, direction_vector, speed, already_moved):
        for rider in riders:
            if rider in already_moved:
                continue
            rider.position = (rider.position + speed * direction_vector).tolist()
            rider._moved = True
            already_moved.add(rider)

            other_riders = []
            for other in GameLogic.game_objects:
                if other == rider or other == self.game_object:
                    continue

                if not GameLogic.collide(rider, GameLogic.game_objects[other]):
                    continue

                if GameLogic.game_objects[other] in rider.collisions:
                    continue

                other_riders.append(GameLogic.game_objects[other])

            if other_riders:
                self.move_riders(other_riders, direction_vector, speed, already_moved)
