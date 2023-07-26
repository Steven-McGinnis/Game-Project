from behavior import Behavior
from game_logic import GameLogic

class Friction(Behavior):
    def __init__(self, coefficient):
        super(Friction, self).__init__()

        self.coefficient = coefficient

    def tick(self):
        if not self.game_object.get_property("falling", False):  # type: ignore
            velocity = self.game_object.get_property('velocity', [0.0, 0.0, 0.0]) # type: ignore
            velocity[0] *= (1 - self.coefficient)
            velocity[2] *= (1 - self.coefficient)
            
            if abs(velocity[0]) < 0.01:
                velocity[0] = 0
            if abs(velocity[2]) < 0.01:
                velocity[2] = 0

            self.game_object.set_property('velocity', velocity) # type: ignore
