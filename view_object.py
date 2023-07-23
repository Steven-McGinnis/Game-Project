from OpenGL.GL import *
from OpenGL.GLU import *

class ViewObject:
    def __init__(self, game_object):
        self.game_object = game_object

    def display(self):
        glPushMatrix()

        glTranslatef(*self.game_object.position)

        glRotatef(self.game_object.x_rotation, 1, 0, 0)
        glRotatef(self.game_object.y_rotation, 0, 1, 0)
        glRotatef(self.game_object.z_rotation, 0, 0, 1)

        glPushName(self.game_object.id)
        self.draw()
        glPopName()

        glPopMatrix()
        

    def draw(self):
        pass