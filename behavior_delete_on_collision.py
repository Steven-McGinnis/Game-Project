import json
from game_logic import GameLogic
from pubsub import pub
from behavior import Behavior
from logger import Logger


class DeleteOnCollision(Behavior):
    def __init__(self, logger=None):
        super(DeleteOnCollision, self).__init__()
        pub.subscribe(self.collided, "collision")
        self.logger = logger if logger is not None else Logger()

        # Load the identifier-to-message mapping from the JSON file
        with open("collision.json", "r") as f:
            self.identifier_to_message = json.load(f)

    def collided(self, obj):
        # check if the object has been collided with before
        if obj.collided:
            return  # don't process the object
        obj.collided = True  # set the flag to indicate that it's been collided with

        if obj.id in GameLogic.game_objects:
            identifier = obj.identifier
            message = self.identifier_to_message.get(identifier)
            if message:
                self.logger.add_log(message)
                print(message)
                pub.sendMessage(identifier)

            # This sends a message to delete from the view
            GameLogic.delete_object(obj)  # this is the fixed line
