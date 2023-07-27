from behavior import Behavior
from game_logic import GameLogic
from sounds import Sounds

class Disappear(Behavior):
    def __init__(self, name, value, sound=None):
        super(Disappear, self).__init__()

        self.name = name
        self.value = value
        self.sound = sound
        self.sound_played = False

    def tick(self):
        if self.game_object.get_property(self.name) == self.value: # type: ignore
            if self.sound and not self.sound_played:
                Sounds.play_sound(self.sound, self.delete_object)
                self.sound_played = True


    def delete_object(self):
        GameLogic.delete_object(self.game_object)