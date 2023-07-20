from OpenGL.GL import *
from OpenGL.GLU import *

class ViewObject:
    def __init__(self, game_object):
        self.game_object = game_object

    def display(self):
        glPushMatrix()

        glTranslatef(*self.game_object.position)

        self.draw()

        glPopMatrix()
        

    def draw(self):
        pass