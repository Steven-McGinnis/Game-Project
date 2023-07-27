from behavior import Behavior

class EnableHighlight(Behavior):
    def hover(self, game_object):
        self.game_object._highlight = True # type: ignore


class HighlightColor(Behavior):
    def __init__(self, color):
        super(HighlightColor, self).__init__()
        
        self.highlight_color = color

    def connect(self, game_object):
        super(HighlightColor, self).connect(game_object)

        self.game_object.set_property("highlight_color", self.highlight_color) # type: ignore
