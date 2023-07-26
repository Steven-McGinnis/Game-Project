from behavior import Behavior
from pubsub import pub
import numpy as np

class IceSlide(Behavior):
    def __init__(self, friction_coefficient):
        super(IceSlide, self).__init__()
        self.friction_coefficient = friction_coefficient

    def tick(self):
        if not self.game_object.get_property('falling', False): # type: ignore
            velocity = self.game_object.get_property('velocity', np.array([0.0, 0.0, 0.0])) # type: ignore
            velocity -= self.friction_coefficient * velocity

            if np.linalg.norm(velocity) < 0.01:
                velocity = np.array([0.0, 0.0, 0.0])

            self.game_object.set_property('velocity', velocity) # type: ignore
