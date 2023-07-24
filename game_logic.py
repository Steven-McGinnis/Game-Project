from game_object import GameObject
from behavior_x_rotation import XRotation
from behavior_y_rotation import YRotation
from behavior_z_rotation import ZRotation
from behavior_mouse_rotation import MouseRotation
from behavior_key_move import KeyMove
from behavior_collision import BlockedByObjects
from behavior_jump import Jump
from behavior_flying import Flying
from behavior_power_up import PowerUpBob
from pubsub import pub
import numpy as np


class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}

        self.next_id = 0

    def tick(self):
        for game_object in self.game_objects:
            if self.game_objects[game_object].moved:
                for other in self.game_objects:
                    if self.game_objects[game_object] == self.game_objects[other]:
                        continue

                    if self.collide(
                        self.game_objects[game_object], self.game_objects[other]
                    ):
                        self.game_objects[game_object].collisions.append(
                            self.game_objects[other]
                        )

        for id in self.game_objects:
            self.game_objects[id].tick()

    def create_object(self, kind, position, size):
        obj = GameObject(kind, self.next_id, position, size)
        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage("create", game_object=obj)
        return obj

    def load_world(self):
        self.create_environment()
        self.create_level_objects()

        player = self.load_player()

    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]

        return None

    def set_property(self, key, value):
        self.properties[key] = value

    def collide(self, object1, object2):
        if object1.kind == "floor" or object2.kind == "floor":
            radius1 = min(object1.size)
            radius2 = min(object2.size)
        else:
            radius1 = max(object1.size)
            radius2 = max(object2.size)

        mypos = np.array(object1.position)
        otherpos = np.array(object2.position)

        distance = np.linalg.norm(mypos - otherpos)
        direction_vector = (mypos - otherpos) / distance

        return distance < radius1 + radius2

    def load_player(self):
        player = self.create_object("player", [0.0, 0.0, 0.0], [1.0, 1.0, 1.0])
        player.add_behavior(KeyMove(0.1))
        player.add_behavior(MouseRotation(0.1))
        player.add_behavior(BlockedByObjects())
        player.add_behavior(Jump(10, 0.5))
        # player.add_behavior(
        #     Flying(0.9, 0.5)
        # )  # 3.0 for movement speed, 0.5 for rotation speed
        return player

    def create_environment(self):
        ground = self.create_object("floor", [0.0, -1.1, 0.0], [50.0, 50, 50.0])
        ground._x_rotation = 90

        floor = self.create_object("wood_floor", [0.0, -1.0, 0.0], [1.0, 1.0, 1.0])
        floor._x_rotation = 90

        wall = self.create_object("outer_wall", [-37.5, 5, 50], [1.0, 1.0, 1.0])
        wall = self.create_object("outer_wall", [-10, 5, 50], [1.0, 1.0, 1.0])

    def create_level_objects(self):
        sphere = self.create_object("sphere", [15, 0, -10], [1.0, 1.0, 1.0])
        sphere.add_behavior(XRotation(0.5))
        sphere.add_behavior(PowerUpBob(0.5, 1))
