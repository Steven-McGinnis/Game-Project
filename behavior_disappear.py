from behavior import Behavior
from game_logic import GameLogic

class Disappear(Behavior):
    def __init__(self, name, value):
        super(Disappear, self).__init__()

        self.name = name
        self.value = value

    def tick(self):
        if self.game_object.get_property(self.name) == self.value:
            GameLogic.delete_object(self.game_object)