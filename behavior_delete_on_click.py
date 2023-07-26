import json
from pubsub import pub
from behavior import Behavior
from game_logic import GameLogic
from logger import Logger

class DeleteOnClick(Behavior):
    def __init__(self):
        super(DeleteOnClick, self).__init__()

        # Load the identifier-to-message mapping from the JSON file
        with open('collision.json', 'r') as f:
            self.identifier_to_message = json.load(f)

    def clicked(self):
        if self.game_object.id in GameLogic.game_objects:  # type: ignore
            identifier = self.game_object.identifier # type: ignore
            message = self.identifier_to_message.get(identifier)
            if message:
                print(message)
                pub.sendMessage(identifier)

            # This sends a message to delete from the view 
            pub.sendMessage("delete", id=self.game_object.id) # type: ignore
