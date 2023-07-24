from behavior import Behavior
from pubsub import pub
import numpy as np
import math

class BlockedByObjects(Behavior):
    def tick(self):
        if self.game_object.collisions: # type: ignore
            mypos = np.array(self.game_object.position) # type: ignore

            for other in self.game_object.collisions: # type: ignore
                otherpos = np.array(other.position)
                distance = np.linalg.norm(mypos - otherpos)
                direction_vector = (mypos - otherpos) / distance
                self.game_object.position = otherpos + (distance + 0.1) * direction_vector # type: ignore
