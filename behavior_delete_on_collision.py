import json
from game_logic import GameLogic
from pubsub import pub
from behavior import Behavior
from logger import Logger
from memory_profiler import profile as Profile
import re


class DeleteOnCollision(Behavior):
    def __init__(self, logger=None):
        super(DeleteOnCollision, self).__init__()
        pub.subscribe(self.collided, "collision")
        self.logger = logger if logger is not None else Logger()

        # Load the identifier-to-message mapping from the JSON file
        with open("collision.json", "r") as f:
            self.identifier_to_message = json.load(f)

    
    def collided(self, obj):
        # Check if the object has been collided with before
        if getattr(obj, 'collided', False):
            return  # Don't process the object if it has already collided

        # Mark the object as collided
        obj.collided = True

        if obj.id in GameLogic.game_objects:
            identifier = obj.identifier

            # Split the identifier to get the base identifier
            split_identifier = re.split(r"(\d+)", identifier, maxsplit=1)

            if len(split_identifier) > 1:
                identifier = split_identifier[0]

            message = self.identifier_to_message.get(identifier)

            if message:
                self.logger.add_log(message)
                pub.sendMessage(identifier)

            # This sends a message to delete from the view
            GameLogic.delete_object(obj)
