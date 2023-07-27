from behavior import Behavior
from game_logic import GameLogic


class Switch(Behavior):
    def __init__(self, name, value, setname, setvalue):
        super(Switch, self).__init__()

        self.name = name
        self.value = value
        self.setname = setname
        self.setvalue = setvalue

    def clicked(self, game_object):
        if game_object.get_property(self.name) == self.value:
            self.game_object.set_property(self.setname, self.setvalue)  # type: ignore
