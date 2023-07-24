from game_object import GameObject
from game_object_player import Player
from game_object_rotating import GameObjectRotating
from pubsub import pub


class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}

        self.next_id = 0

    def tick(self):
        for id in self.game_objects:
            self.game_objects[id].tick()

    def create_object(self, which, kind, position, size):
        obj = which(kind, self.next_id, position, size)
        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage("create", game_object=obj)
        return obj

    def load_world(self):
        self.create_object(GameObjectRotating, "cube", [-2, 0, -10], [1.0, 1.0, 1.0])
        self.create_object(GameObjectRotating, "cube", [2, 0, -10], [5.0, 0.25, 0.25])
        self.create_object(GameObjectRotating, "billboard_cube", [-2, 5, -10], [1.0, 1.0, 1.0])
        self.create_object(GameObjectRotating, "sphere", [0, 0, -10], [1.0, 1.0, 1.0])
        floor = self.create_object(GameObject, "floor", [0, -5, -20], [10.0, 10.0, 10.0])
        floor.x_rotation = -89
        player = self.create_object(Player, "player",[0.0, 0.0, 0.0], [1.0, 1.0, 1.0])

    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]

        return None

    def set_property(self, key, value):
        self.properties[key] = value
