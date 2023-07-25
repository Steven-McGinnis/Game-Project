from OpenGL.GLU import gluNewQuadric, gluSphere, gluQuadricTexture, gluQuadricNormals
from view_object import ViewObject
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image


class SphereView(ViewObject):
    def __init__(self, game_object, radius=0.5, slices=32, stacks=32):
        self.game_object = game_object
        self.radius = radius
        self.slices = slices
        self.stacks = stacks

        if game_object.texture is not None:
            self.texture_id = self.load_texture(game_object.texture)
        else:
            self.texture_id = None

    def load_texture(self, image_path):
        im = Image.open(image_path)
        try:
            ix, iy, image = im.size[0], im.size[1], im.tobytes("raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = im.size[0], im.size[1], im.tobytes("raw", "RGBX", 0, -1)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

        return texture_id

    def draw(self):
        glColor3f(1.0, 1.0, 1.0) if self.texture_id is not None else glColor3f(1.0, 0.0, 0.0)

        if self.texture_id is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluSphere(quadric, self.radius, self.slices, self.stacks)

        if self.texture_id is not None:
            glDisable(GL_TEXTURE_2D)
