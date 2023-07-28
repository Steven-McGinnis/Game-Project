from behavior import Behavior
from game_logic import GameLogic
from sounds import Sounds
from pubsub import pub

class Shoot(Behavior):
    def __init__(self, sound=None):
        super(Shoot, self).__init__()
        self.sound = sound
        self.connected_object = None

    def connect(self, game_object):
        super(Shoot, self).connect(game_object)
        self.connected_object = game_object

    def clicked(self, game_object):
        if self.sound:
            Sounds.play_sound(self.sound)
        self.delete_object()

    def delete_object(self):
        if self.game_object.id in GameLogic.game_objects: # type: ignore
            enemy_position = self.game_object.position # type: ignore
            GameLogic.delete_object(self.game_object)
            GameLogic.total_enemies -= 1
            pub.sendMessage("enemy_destroyed",  position=enemy_position)
