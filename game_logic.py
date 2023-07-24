from game_object_rotating import GameObjectRotating
from game_object import GameObject
from pubsub import pub

class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}

        self.next_id = 0 

    def tick(self):
        for id in self.game_objects:
            self.game_objects[id].tick()

    def create_object(self, kind, position, type):
        if type == "rotating":
            obj = GameObjectRotating(kind, self.next_id, position)
        elif type == "standard":
            obj = GameObject(kind, self.next_id, position)
        else:
            obj = GameObject(kind, self.next_id, position)
        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage("create", game_object=obj)
        return obj

    def load_world(self):
        self.create_object("cube", [-2, 0, -10], "rotating")
        obj = self.create_object("cube", [2, 0, -10], "rotating")
        self.create_object("billboard_cube", [-2, 5, -10], "rotating")
        self.create_object("sphere", [0, 0, -10],"standard")
        # obj.y_rotation = 45

        floor = self.create_object("floor", [0, -5, -20], "standard")
        floor.x_rotation = -89

    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]
        
        return None

    def set_property(self, key, value): 
        self.properties[key] = value