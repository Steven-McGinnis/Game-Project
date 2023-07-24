from behavior import Behavior

class XRotation(Behavior):
    def __init__(self, speed):
        super(XRotation, self).__init__()
        self.speed = speed

    def tick(self):
        if self.game_object is not None:
            self.game_object.x_rotation += self.speed
