import random
from pubsub import pub
from behavior import Behavior
from game_logic import GameLogic

class SpawnPowerUp(Behavior):
    def __init__(self):
        super(SpawnPowerUp, self).__init__()
        pub.subscribe(self.on_enemy_destroyed, "enemy_destroyed")
        self.test = True

    def on_enemy_destroyed(self, position):
        if self.test:
            powerup = GameLogic.create_powerup(position)
        else:
            roll = random.randint(1, 20)  # Roll a d20
            if roll == 20:
                powerup = GameLogic.create_powerup(position)
