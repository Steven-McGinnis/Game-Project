from behavior import Behavior

class Gravity(Behavior):
    def __init__(self, gravity_force):
        self.gravity_force = gravity_force

    def tick(self):
        self.game_object.position[1] -= self.gravity_force # type: ignore
