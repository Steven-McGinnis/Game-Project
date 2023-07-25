from behavior import Behavior
from pubsub import pub
import numpy as np
from game_logic import GameLogic


class Gravity(Behavior):
    def __init__(self, speed):
        super(Gravity, self).__init__()

        self.speed = speed
        self.old_y = 0.0

    def tick(self):
        if self.game_object.position[1] <= 0.0:  # type: ignore
            self.game_object.set_property("falling", False)  # type: ignore
            self.game_object.position[1] = 0.0  # type: ignore
            return
        
        self.old_y = self.game_object.position[1]  # type: ignore
        self.game_object.position[1] -= self.speed  # type: ignore
        
        for other in GameLogic.game_objects:
            if not GameLogic.collide(self.game_object, GameLogic.game_objects[other]): 
                continue

            if GameLogic.game_objects[other] in self.game_object.collisions: # type: ignore
                continue

            self.game_object.position[1] += self.speed # type: ignore
            self.game_object.set_property("falling", False)  # type: ignore
            return
        
        if self.old_y != self.game_object.position[1]:  # type: ignore
            self.game_object.set_property("falling", True)  # type: ignore
        else:
            self.game_object.set_property("falling", False)  # type: ignore

        
        self.game_object.set_property('y_velocity', self.game_object.get_property('y_velocity', 0.0) + self.speed)  # type: ignore
        self.game_object._moved = True  # type: ignore
