from pubsub import pub
from behavior import Behavior
from game_logic import GameLogic

class DeleteOnClick(Behavior):
    def __init__(self):
        super(DeleteOnClick, self).__init__()

    def clicked(self):
        if self.game_object.id in GameLogic.game_objects:  # type: ignore
            identifier = self.game_object.identifier # type: ignore
            if identifier == "power_up":
                print("POWER UP")
                pub.sendMessage("power_up")

            # This sends a message to delete from the view 
            pub.sendMessage("delete", id=self.game_object.id) # type: ignore

