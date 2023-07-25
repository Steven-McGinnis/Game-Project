from behavior import Behavior


class Gravity(Behavior):
    def __init__(self, speed):
        super(Gravity, self).__init__()

        self.speed = speed

    def tick(self):
        self.game_object.position[1] -= self.speed  # type: ignore
        self.game_object._moved = True  # type: ignore
