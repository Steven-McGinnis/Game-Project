from view_object import ViewObject
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image


class WorldView(ViewObject):
    def __init__(self, game_object):
        self.game_object = game_object
        if game_object.texture is not None:
            self.texture_id = self.load_texture(game_object.texture)
            print("Loaded texture", game_object.texture)
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

        glBegin(GL_QUADS)
        # Front face
        glNormal3f(0.0, 0.0, 1.0)
        glTexCoord2f(0.0, 1.0); glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(0.5, 0.5, 0.5)
        
        glColor3f(1.0, 1.0, 1.0) if self.texture_id is not None else glColor3f(0.0, 1.0, 0.0)
        # Left face
        glNormal3f(-1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(-0.5, 0.5, -0.5)
        
        glColor3f(1.0, 1.0, 1.0) if self.texture_id is not None else glColor3f(0.0, 0.0, 1.0)
        # Back face
        glNormal3f(0.0, 0.0, -1.0)
        glTexCoord2f(0.0, 1.0); glVertex3d(-0.5, 0.5, -0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(0.5, 0.5, -0.5)

        glColor3f(1.0, 1.0, 1.0) if self.texture_id is not None else glColor3f(1.0, 1.0, 0.0)
        # Right face
        glNormal3f(1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3d(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(0.5, 0.5, -0.5)

        glColor3f(1.0, 1.0, 1.0) if self.texture_id is not None else glColor3f(0.0, 1.0, 1.0)
        # Top face
        glNormal3f(0.0, 1.0, 0.0)
        glTexCoord2f(0.0, 100.0); glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(0.5, 0.5, 0.5)
        glTexCoord2f(100.0, 0.0); glVertex3d(0.5, 0.5, -0.5)
        glTexCoord2f(100.0, 100.0); glVertex3d(-0.5, 0.5, -0.5)

        glColor3f(1.0, 1.0, 1.0) if self.texture_id is not None else glColor3f(1.0, 1.0, 1.0)
        # Bottom face
        glNormal3f(0.0, -1.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(-0.5, -0.5, -0.5)
        glEnd()

        if self.texture_id is not None:
            glDisable(GL_TEXTURE_2D)
