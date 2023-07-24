class Behavior:
    def __init__(self):
        self.game_object = None

    def connect(self, game_object):
        self.game_object = game_object

    def tick(self):
        pass