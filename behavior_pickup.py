from behavior import Behavior
from game_logic import GameLogic

class Pickup(Behavior):
    def __init__(self, name, value):
        super(Pickup, self).__init__()

        self.name = name
        self.value = value

    def clicked(self, game_object):
        game_object.set_property(self.name, self.value)
        GameLogic.delete_object(self.game_object) # type: ignore

        