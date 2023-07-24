from game_object import GameObject
from behavior_x_rotation import XRotation
from behavior_y_rotation import YRotation
from behavior_z_rotation import ZRotation
from behavior_mouse_rotation import MouseRotation
from behavior_key_move import KeyMove
from behavior_collision import BlockedByObjects
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
                
                    if self.collide(self.game_objects[game_object], self.game_objects[other]):
                        self.game_objects[game_object].collisions.append(self.game_objects[other])

        for id in self.game_objects:
            self.game_objects[id].tick()

    def create_object(self, kind, position, size):
        obj = GameObject(kind, self.next_id, position, size)
        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage("create", game_object=obj)
        return obj

    def load_world(self):
        cube = self.create_object ("cube",  [-15,0,-10],[0.25, 10.0, 0.25])
        cube.add_behavior(XRotation(0.5))
        cube.add_behavior(YRotation(0.5))
        cube.add_behavior(ZRotation(0.5))

        player = self.load_player()


    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]

        return None

    def set_property(self, key, value):
        self.properties[key] = value

    def collide(self, object1, object2):
        radius1 = max(object1.size)
        mypos = np.array(object1.position)
        otherpos = np.array(object2.position)

        distance = np.linalg.norm(mypos - otherpos)
        direction_vector = (mypos - otherpos) / distance

        max_direction = max(direction_vector, key=abs)
        indices = [i for i , j in enumerate(direction_vector) if j == max_direction]
        sizes = [object2.size[j] for i, j in enumerate(indices)]
        radius2 = max(sizes)

        return distance < radius1 + radius2

    def load_player(self):
        player = self.create_object("player",[0.0, 0.0, 0.0], [1.0, 1.0, 1.0])
        player.add_behavior(KeyMove(0.1))
        player.add_behavior(MouseRotation(0.1))
        player.add_behavior(BlockedByObjects())
        return player
    
    