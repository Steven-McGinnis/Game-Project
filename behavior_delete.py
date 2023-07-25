from behavior import Behavior
from pubsub import pub

class DeleteOnCollision(Behavior):
    def tick(self):
        if self.game_object.collisions:  # type: ignore
            print("Collision detected")
            pub.sendMessage("delete", game_object=self.game_object)
            self.game_object.collisions = []  # Clear the collision list for next tick