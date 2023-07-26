from behavior import Behavior
from pubsub import pub
from game_logic import GameLogic

class Portal(Behavior):
    def __init__(self):
        super(Portal, self).__init__()
        pub.subscribe(self.collided, "portal")

    def collided(self):
        GameLogic.load_world("level2.json")