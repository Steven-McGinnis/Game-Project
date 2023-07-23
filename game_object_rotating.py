from game_object import GameObject

class GameObjectRotating(GameObject):
    def __init__(self, kind, id, position):
        super(GameObjectRotating, self).__init__(kind, id, position)

        self.allow_rotation = True

    def tick(self):
        if self.allow_rotation:
            self.y_rotation += 0.5
            self.x_rotation += 0.5
            # self.z_rotation += 0.5

    def clicked(self):
        self.allow_rotation = not self.allow_rotation