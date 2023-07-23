import pygame
from view_object import ViewObject
from OpenGL.GL import *
from OpenGL.GLU import *

class FloorView(ViewObject):
    def __init__(self, game_object, texture_file):
        super().__init__(game_object)
        self.texture = self.load_texture(texture_file)

    def load_texture(self, texture_file):
        texture_surface = pygame.image.load(texture_file)
        texture_data = pygame.image.tostring(texture_surface, 'RGBA')
        width, height = texture_surface.get_size()

        texid = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        return texid

    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-50.0, -50.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(50.0, -50.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(50.0, 50.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-50.0, 50.0, 0.0)
        glEnd()

        glDisable(GL_TEXTURE_2D)
