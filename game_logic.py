from game_object import GameObject
from pubsub import pub
import json
import importlib


class GameLogic:
    properties = {}
    game_objects = {}
    identifier_index = {}
    files = {}
    deletions = []
    level_data = {}
    filename = None

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
    def create_object(data):
        obj = GameObject(GameLogic.next_id, data)
        GameLogic.next_id += 1
        GameLogic.game_objects[obj.id] = obj

        if "identifier" in data:
            GameLogic.identifier_index[data['identifier']] = obj

        pub.sendMessage("create", game_object=obj)
        return obj

    @staticmethod
    def load_world(filename):
        pub.sendMessage("delete_all")
        GameLogic.game_objects = {}
        GameLogic.filename = filename

        with open(filename) as infile:
            level_data = json.load(infile)
            GameLogic.level_data = level_data

            if not "objects" in level_data:
                return False

            for game_object in level_data["objects"]:
                obj = GameLogic.create_object(game_object)

                if "behaviors" not in game_object:
                    continue

                for behavior in game_object["behaviors"]:
                    module = importlib.import_module(level_data["behaviors"][behavior])
                    class_ = getattr(module, behavior)
                    instance = class_(*game_object["behaviors"][behavior])
                    instance.arguments = game_object["behaviors"][behavior]

                    obj.add_behavior(instance)

                for file in level_data['files']:
                    GameLogic.files[file] = level_data['files'][file]

                if "level" in level_data:
                    if 'music' in level_data['level']:
                        from sounds import Sounds
                        Sounds.play_music(level_data['level']['music'])

    @staticmethod
    def save_world():
        if 'objects' in GameLogic.level_data:
            del GameLogic.level_data['objects']

        GameLogic.level_data['objects'] = []

        for game_object in GameLogic.game_objects:
            GameLogic.save_object(GameLogic.game_objects[game_object])

        with open(GameLogic.filename, 'w') as outfile:
            json.dump(GameLogic.level_data, outfile, sort_keys=True, indent=4)

    @staticmethod
    def save_object(game_object):
        data = {}

        data['kind'] = game_object.kind
        data['position'] = game_object.position
        data['size'] = game_object.size

        if game_object.faces:
            data['faces'] = game_object.faces
        
        if game_object.identifier:
            data['identifier'] = game_object.identifier

        if game_object.texture:
            data['texture'] = game_object.texture

        if game_object.x_rotation or game_object.y_rotation or game_object.z_rotation:
            data['rotation'] = [game_object.x_rotation, game_object.y_rotation, game_object.z_rotation]

        data['behaviors'] = {}

        for behavior in game_object.behaviors:
            data['behaviors'][behavior] = game_object.behaviors[behavior].arguments

        GameLogic.level_data['objects'].append(data)

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
            if obj.identifier:
                del GameLogic.identifier_index[obj.identifier]

            if obj.id in GameLogic.game_objects:  # Check before deletion
                del GameLogic.game_objects[obj.id]
                pub.sendMessage("delete", game_object=obj)

        GameLogic.deletions = []

    @staticmethod
    def get_object(id):
        result = None

        if id in GameLogic.identifier_index:
            result = GameLogic.identifier_index[id]

        if id in GameLogic.game_objects:
            result = GameLogic.game_objects[id]

        return result

    @staticmethod
    def order_objects(obj1, obj2):
        if obj1.kind == "player":
            return obj1, obj2
        return obj2, obj1

    @staticmethod
    def collisionType(obj1, obj2):
        player, other = GameLogic.order_objects(obj1, obj2)

        if other.identifier in ["power_up", "portal", "inverse"]:
            print(other.identifier, other.identifier)
            pub.sendMessage("collision", obj=other)


