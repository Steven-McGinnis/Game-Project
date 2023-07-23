import pygame
from OpenGL.GL import * # nosec
from OpenGL.GLU import * # nosec
from view_object import ViewObject

class BillboardCubeView(ViewObject):
    def __init__(self, game_object):
        super().__init__(game_object) 

        self.front_texture = self.create_texture("Front")
        self.back_texture = self.create_texture("Back")
        self.left_texture = self.create_texture("Left")
        self.right_texture = self.create_texture("Right")
        self.top_texture = self.create_texture("Top")
        self.bottom_texture = self.create_texture("Bottom")

    def create_texture(self, text):
        img = pygame.font.SysFont("Arial", 25).render(text, True, (0, 255, 0), (255, 255, 0))
        w, h = img.get_size()
        texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)  # type: ignore
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        return texture

    def draw(self):
            glEnable(GL_TEXTURE_2D)

            # Front face
            glBindTexture(GL_TEXTURE_2D, self.front_texture)
            self.draw_face(0.0, 0.0, 1.0, (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0), (1.0, -1.0, 1.0), (1.0, 1.0, 1.0))
            
            # Back face
            glBindTexture(GL_TEXTURE_2D, self.back_texture)
            self.draw_face(0.0, 0.0, -1.0, (-1.0, 1.0, -1.0), (-1.0, -1.0, -1.0), (1.0, -1.0, -1.0), (1.0, 1.0, -1.0))
            
            # Left face
            glBindTexture(GL_TEXTURE_2D, self.left_texture)
            self.draw_face(-1.0, 0.0, 0.0, (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0), (-1.0, -1.0, -1.0), (-1.0, 1.0, -1.0))

            # Right face
            glBindTexture(GL_TEXTURE_2D, self.right_texture)
            self.draw_face(1.0, 0.0, 0.0, (1.0, 1.0, 1.0), (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (1.0, 1.0, -1.0))

            # Top face
            glBindTexture(GL_TEXTURE_2D, self.top_texture)
            self.draw_face(0.0, 1.0, 0.0, (-1.0, 1.0, 1.0), (1.0, 1.0, 1.0), (1.0, 1.0, -1.0), (-1.0, 1.0, -1.0))

            # Bottom face
            glBindTexture(GL_TEXTURE_2D, self.bottom_texture)
            self.draw_face(0.0, -1.0, 0.0, (-1.0, -1.0, 1.0), (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, -1.0, -1.0))

            glDisable(GL_TEXTURE_2D)

    def draw_face(self, nx, ny, nz, v1, v2, v3, v4):
        glBegin(GL_QUADS)
        glNormal3f(nx, ny, nz)
        glTexCoord2f(0.0, 1.0); glVertex3d(*v1)
        glTexCoord2f(0.0, 0.0); glVertex3d(*v2)
        glTexCoord2f(1.0, 0.0); glVertex3d(*v3)
        glTexCoord2f(1.0, 1.0); glVertex3d(*v4)
        glEnd()