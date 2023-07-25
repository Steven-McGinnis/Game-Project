from behavior import Behavior
from pubsub import pub
import numpy as np
import math


class BlockedByObjects(Behavior):
    def tick(self):
        if self.game_object.collisions:  # type: ignore
            mypos = np.array(self.game_object.position)  # type: ignore

            for other in self.game_object.collisions:  # type: ignore
                otherpos = np.array(other.position)
                distance = np.linalg.norm(mypos - otherpos)
                direction_vector = (mypos - otherpos) / distance

                max_direction = max(direction_vector, key=abs)
                indices = [
                    i for i, j in enumerate(direction_vector) if j == max_direction
                ]

                velocity = 0.0
                for index in indices:
                    if index == 0:
                        velocity = max(velocity, self.game_object.get_property("x_velocity", 0.1))  # type: ignore

                    if index == 1:
                        velocity = max(velocity, self.game_object.get_property("y_velocity", 0.1))  # type: ignore

                    if index == 2:
                        velocity = max(velocity, self.game_object.get_property("z_velocity", 0.1))  # type: ignore

                self.game_object.position = otherpos + (distance + velocity) * direction_vector  # type: ignore
