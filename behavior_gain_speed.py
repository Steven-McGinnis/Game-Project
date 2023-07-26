from behavior import Behavior
from game_logic import GameLogic
from pubsub import pub
from behavior_key_move import KeyMove

class GainSpeed(Behavior):
    def __init__(self):
        super(GainSpeed, self).__init__()
        pub.subscribe(self.gain_speed, "power_up")
        self.count = 0
        self.speedup = False

    def gain_speed(self):
        for behavior in self.game_object.behaviors: # type: ignore
            if isinstance(behavior, KeyMove):
                behavior.speed += .5
                self.speedup = True

    def tick(self):
        if self.speedup:
            self.count += 1
            if self.count == 100:
                for behavior in self.game_object.behaviors: # type: ignore
                    if isinstance(behavior, KeyMove):
                        behavior.speed -= .5
                self.count = 0
                self.speedup = False