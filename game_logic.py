from game_object import GameObject
from pubsub import pub
import json
import importlib
from memory_profiler import profile
import time
import random


class GameLogic:
    properties = {}
    game_objects = {}
    identifier_index = {}
    files = {}
    deletions = []
    level_data = {}
    filename = None
    game_state = "None"
    round_timer_start = None
    round_started = False
    round_wait = False
    spawned = False
    round = 0
    enemies = 20
    total_enemies = 0
    round_timer = 0
    enemy_speed = 0.01

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

        if not GameLogic.round_started:
            GameLogic.in_between_round()
        
        if GameLogic.round_started:
            GameLogic.game_round()

        GameLogic.process_deletions()

    @staticmethod
    def create_object(data):
        obj = GameObject(GameLogic.next_id, data)
        GameLogic.next_id += 1
        GameLogic.game_objects[obj.id] = obj

        if "identifier" in data:
            GameLogic.identifier_index[data["identifier"]] = obj

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

                for file in level_data["files"]:
                    GameLogic.files[file] = level_data["files"][file]

                if "level" in level_data:
                    if "music" in level_data["level"]:
                        from sounds import Sounds
                        Sounds.play_music(level_data["level"]["music"])

                        

    @staticmethod
    def save_world():
        if "objects" in GameLogic.level_data:
            del GameLogic.level_data["objects"]

        GameLogic.level_data["objects"] = []

        for game_object in GameLogic.game_objects:
            GameLogic.save_object(GameLogic.game_objects[game_object])

        with open(GameLogic.filename, "w") as outfile:  # type: ignore
            outfile.write(GameLogic.jsonprint(GameLogic.level_data))

    @staticmethod
    def save_object(game_object):
        data = {}

        data["kind"] = game_object.kind
        data["position"] = game_object.position
        data["size"] = game_object.size

        if game_object.faces:
            data["faces"] = game_object.faces

        if game_object.identifier:
            data["identifier"] = game_object.identifier

        if game_object.texture:
            data["texture"] = game_object.texture

        if game_object.x_rotation or game_object.y_rotation or game_object.z_rotation:
            data["rotation"] = [
                game_object.x_rotation,
                game_object.y_rotation,
                game_object.z_rotation,
            ]

        data["behaviors"] = {}

        for behavior in game_object.behaviors:
            data["behaviors"][behavior] = game_object.behaviors[behavior].arguments

        GameLogic.level_data["objects"].append(data)

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

    @staticmethod
    def replace(data):
        import uuid

        replacements = []
        objects = []

        for obj in data["objects"]:
            replacement = uuid.uuid4().hex
            replacements.append((f'"{replacement}"', json.dumps(obj)))

            objects.append(f"{replacement}")

        data["objects"] = objects

        return data, replacements

    @staticmethod
    def jsonprint(data):
        import copy

        data = copy.deepcopy(data)

        data, replacements = GameLogic.replace(data)
        result = json.dumps(data, indent=4)

        for old, new in replacements:
            result = result.replace(old, new)

        return result

    @staticmethod
    def in_between_round():
        if not GameLogic.round_started:
            # If You Havnt Waited for the Round yet
            if GameLogic.round_timer == 0 and not GameLogic.round_wait:
                GameLogic.round_timer = 5
                GameLogic.round_timer_start = time.time()
                GameLogic.game_state = "round_wait"
                GameLogic.round_wait = True
            
            # If You Have Waited for the Round and the timer has reached Zero Start the Round
            elif GameLogic.round_timer <= 0 and GameLogic.round_wait:
                GameLogic.round_started = True
                GameLogic.game_state = "round_start"

            # If You Have Waited for the Round and the timer has not reached Zero Continue to Wait
            elif GameLogic.round_timer_start is not None:
                elapsed_time = time.time() - GameLogic.round_timer_start
                GameLogic.round_timer = max(0, GameLogic.round_timer - elapsed_time)
                GameLogic.round_timer_start = time.time()

    @staticmethod
    def game_round():
        # If the Round has just started
        # Create the variable for the next round
        if GameLogic.game_state == "round_start":
            GameLogic.round += 1
            GameLogic.enemies = 5 * GameLogic.round
            GameLogic.game_state = "round"
        # If the Round is in play
        # Spawn Enemies
        # Check for Round End
        elif GameLogic.game_state == "round":
            # Spawn Enemies
            if not GameLogic.spawned:
                for _ in range(GameLogic.enemies):
                    GameLogic.create_enemy()
                    GameLogic.total_enemies += 1
                GameLogic.spawned = True
            
            # Check for Round End
            if GameLogic.total_enemies == 0:
                GameLogic.round_started = False
                GameLogic.round_wait = False
                GameLogic.spawned = False
                GameLogic.round_timer = 0
                GameLogic.game_state = "round_end"

            

            

    @staticmethod
    def create_enemy(safety_distance=50):
        # Get the player's position
        player = GameLogic.get_object("player")
        player_pos = player.position if player else [0, 0, 0]

        # Create a random position away from the player
        random_x = player_pos[0] + random.uniform(-1, 1) * safety_distance
        random_z = player_pos[2] + random.uniform(-1, 1) * safety_distance

        # Keep the generated position within the specified range
        min_x, max_x = -50, 50
        min_z, max_z = -50, 50
        random_x = max(min_x, min(max_x, random_x))
        random_z = max(min_z, min(max_z, random_z))

        position = [random_x, 0.0, random_z]
        unique_id = str(GameLogic.next_id)
        # Define the enemy data
        enemy_data = {
            "kind": "cube2",
            "position": position,
            "identifier": "enemy" + unique_id,
            "faces": {
                "front": {"type": "texture", "value": "zombie"},
                "back": {"type": "texture", "value": "zombie"},
                "left": {"type": "texture", "value": "zombie"},
                "right": {"type": "texture", "value": "zombie"},
            },
            "behaviors": {
                "Goto": ["player", GameLogic.enemy_speed, 1.0],
                "Shoot": ["zombieDeath"]
            }
        }

        # Create the enemy using create_object function
        enemy = GameLogic.create_object(enemy_data)
        
        # add behaviors to enemy object as in load_world
        for behavior in enemy_data["behaviors"]:
            module = importlib.import_module(GameLogic.level_data["behaviors"][behavior])
            class_ = getattr(module, behavior)
            instance = class_(*enemy_data["behaviors"][behavior])
            instance.arguments = enemy_data["behaviors"][behavior]
            enemy.add_behavior(instance)
            
        return enemy
