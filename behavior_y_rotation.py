from behavior import Behavior

class YRotation(Behavior):
    def __init__(self, speed):
        super(YRotation, self).__init__()
        self.speed = speed

    def tick(self):
        if self.game_object is not None:
            self.game_object.y_rotation += self.speed
