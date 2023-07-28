from behavior import Behavior
from game_logic import GameLogic
from sounds import Sounds

class Shoot(Behavior):
    def __init__(self, sound=None):
        super(Shoot, self).__init__()
        self.sound = sound
        self.connected_object = None

    def connect(self, game_object):
        super(Shoot, self).connect(game_object)
        self.connected_object = game_object

    def clicked(self, game_object):
        print(self.connected_object.identifier)
        if self.connected_object.identifier == 'enemy':
            print("Shoot clicked")
            print(self.sound)
            if self.sound:
                Sounds.play_sound(self.sound, self.delete_object)

    def delete_object(self):
        GameLogic.delete_object(self.connected_object)
