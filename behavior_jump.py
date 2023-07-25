from behavior import Behavior
from pubsub import pub


class Jump(Behavior):
    def __init__(self, speed, adjust):
        super(Jump, self).__init__()

        self.speed = speed
        self.adjust = adjust
        self.current = self.speed

        self.jumping = False

        pub.subscribe(self.jump, "key-jump")

    def jump(self):
        if not self.game_object.get_property("falling"):  # type: ignore
            self.jumping = True

    def tick(self):
        if not self.jumping:
            return

        if self.current <= 0.0:
            self.jumping = False
            self.current = self.speed
            return

        self.game_object.position[1] += self.current  # type: ignore
        self.current -= self.adjust
        self.game_object._moved = True  # type: ignore
        self.current -= self.adjust
