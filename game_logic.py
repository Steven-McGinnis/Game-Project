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
import json
import importlib


class GameLogic:
    properties = {}
    game_objects = {}
    deletions = []

    next_id = 0

    @staticmethod
    def tick():
        for game_object in GameLogic.game_objects.values():
            if game_object.moved:
                for other in GameLogic.game_objects.values():
                    if game_object != other and GameLogic.collide(game_object, other):
                        game_object.collisions.append(other)
                        GameLogic.collisionType(game_object, other)

        for game_object in GameLogic.game_objects.values():
            game_object.tick()

        GameLogic.process_deletions()

    @staticmethod
    def create_object(
        kind, position, size, texture=None, rotation=None, identifier=None
    ):
        obj = GameObject(
            kind, GameLogic.next_id, position, size, texture, rotation, identifier
        )
        GameLogic.next_id += 1
        GameLogic.game_objects[obj.id] = obj

        pub.sendMessage("create", game_object=obj)
        return obj

    @staticmethod
    def load_world(filename):
        pub.sendMessage("delete_all")
        GameLogic.game_objects = {}

        with open(filename) as infile:
            level_data = json.load(infile)

            if not "objects" in level_data:
                return False

            for game_object in level_data["objects"]:
                size = [1.0, 1.0, 1.0]
                texture = None
                rotation = None
                identifier = None
                if "size" in game_object:
                    size = game_object["size"]

                if "texture" in game_object:
                    texture = game_object["texture"]

                if "rotation" in game_object:
                    rotation = game_object["rotation"]

                if "identifier" in game_object:
                    identifier = game_object["identifier"]

                obj = GameLogic.create_object(
                    game_object["kind"],
                    game_object["position"],
                    size,
                    texture,
                    rotation,
                    identifier,
                )

                if "behaviors" not in game_object:
                    continue

                for behavior in game_object["behaviors"]:
                    module = importlib.import_module(level_data["behaviors"][behavior])
                    class_ = getattr(module, behavior)
                    instance = class_(*game_object["behaviors"][behavior])

                    obj.add_behavior(instance)

    @staticmethod
    def get_property(key, default=None):
        if key in GameLogic.properties:
            return GameLogic.properties[key]

        return default

    @staticmethod
    def set_property(key, value):
        GameLogic.properties[key] = value

    @staticmethod
    def collide(object1, object2):
        if object1 == object2:
            return False

        # Cuboid detection
        minx1 = object1.position[0] - object1.size[0] / 2.0
        maxx1 = object1.position[0] + object1.size[0] / 2.0
        miny1 = object1.position[1] - object1.size[1] / 2.0
        maxy1 = object1.position[1] + object1.size[1] / 2.0
        minz1 = object1.position[2] - object1.size[2] / 2.0
        maxz1 = object1.position[2] + object1.size[2] / 2.0

        minx2 = object2.position[0] - object2.size[0] / 2.0
        maxx2 = object2.position[0] + object2.size[0] / 2.0
        miny2 = object2.position[1] - object2.size[1] / 2.0
        maxy2 = object2.position[1] + object2.size[1] / 2.0
        minz2 = object2.position[2] - object2.size[2] / 2.0
        maxz2 = object2.position[2] + object2.size[2] / 2.0

        return (
            minx1 < maxx2
            and minx2 < maxx1
            and miny1 < maxy2
            and miny2 < maxy1
            and minz1 < maxz2
            and minz2 < maxz1
        )

    @staticmethod
    def delete_object(obj):
        GameLogic.deletions.append(obj)

    @staticmethod
    def process_deletions():
        for obj in GameLogic.deletions:
            del GameLogic.game_objects[obj.id]
            pub.sendMessage("delete", game_object=obj)

        GameLogic.deletions = []

    @staticmethod
    def collisionType(obj1, obj2):
        if obj1.kind == "player" and obj2.identifier == "power_up":
            print("power up", obj2.identifier)
            pub.sendMessage("collision", obj=obj2)

        elif obj2.kind == "player" and obj1.identifier == "power_up":
            pub.sendMessage("collision", obj=obj1)
            print("power up", obj1.identifier)

        elif obj1.kind == "player" and obj2.identifier == "portal":
            print("New Type", obj2.identifier)
            pub.sendMessage("collision", obj=obj2)

        elif obj2.kind == "player" and obj1.identifier == "portal":
            pub.sendMessage("collision", obj=obj1)
            print("New Type", obj1.identifier)

        elif obj1.kind == "player" and obj2.identifier == "inverse":
            pub.sendMessage("collision", obj=obj2)

        elif obj2.kind == "player" and obj1.identifier == "inverse":
            pub.sendMessage("collision", obj=obj1)
