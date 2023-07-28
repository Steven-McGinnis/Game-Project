from behavior import Behavior
from pubsub import pub
from sounds import Sounds


class InverseGravity(Behavior):
    def __init__(self):
        super(InverseGravity, self).__init__()
        pub.subscribe(self.inverse_gravity, "inverse")
        self.counter = 0
        self.reversed = False

    def inverse_gravity(self):
        Sounds.play_sound("antigrav")
        self.reversed = True
        pub.sendMessage("inverse_gravity")

    def tick(self):
        if self.reversed:
            self.counter += 1
            if self.counter < 1000:
                pass
            else:
                self.reversed = False
                self.counter = 0
                pub.sendMessage("inverse_gravity")
        pass
