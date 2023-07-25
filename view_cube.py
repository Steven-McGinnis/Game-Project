from view_object import ViewObject
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image


class CubeView(ViewObject):
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

        # Generate a new texture ID
        texture_id = glGenTextures(1)
        # Make this texture the current texture.
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Added these two lines
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Upload the image data to OpenGL, converting it to a texture.
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        
        return texture_id

    def draw(self):
        glColor3f(1.0, 1.0, 1.0) if self.texture_id is not None else glColor3f(1.0, 0.0, 0.0)

        if self.texture_id is not None:
            # Enable texture mapping
            glEnable(GL_TEXTURE_2D)
            # Bind the texture
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
        glTexCoord2f(0.0, 1.0); glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(0.5, 0.5, 0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(-0.5, 0.5, -0.5)

        glColor3f(1.0, 1.0, 1.0) if self.texture_id is not None else glColor3f(1.0, 1.0, 1.0)
        # Bottom face
        glNormal3f(0.0, -1.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(-0.5, -0.5, -0.5)
        glEnd()

        if self.texture_id is not None:
            # Disable texture mapping
            glDisable(GL_TEXTURE_2D)
