from view_object import ViewObject
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from textures import Textures


class CubeViewColor(ViewObject):
    def get_color(self, face):
        if face in self.game_object.faces:
            if self.game_object.faces[face]['type'] == 'color':
                return self.game_object.faces[face]['value']
            
        return [0.25, 0.25, 0.25, 1.0]
    
    def get_texture(self, face):
        if face in self.game_object.faces:
            if self.game_object.faces[face]['type'] == 'texture':
                Textures.activate_texture(self.game_object.faces[face]['value'])
    


    def draw(self):
        # Back face
        self.get_texture("back")
        glBegin(GL_QUADS)
        glColor(*self.get_color('back'))
        glNormal3f( 0.0, 0.0, 1.0)
        glTexCoord2f(0.0, 1.0); glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(0.5, 0.5, 0.5)
        glEnd()
        Textures.deactivate_texture("back")
        
        # Left face
        self.get_texture("left")
        glBegin(GL_QUADS)
        glColor(*self.get_color('left'))
        glTexCoord2f(0.0, 1.0); glVertex3d(-0.5, 0.5, -0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(-0.5, 0.5, 0.5)
        glEnd()
        Textures.deactivate_texture("left")
        # Front face
        self.get_texture("front")
        glBegin(GL_QUADS)
        glColor(*self.get_color('front'))
        glTexCoord2f(0.0, 1.0); glVertex3d(0.5, 0.5, -0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(-0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture("front")
        # Right face
        self.get_texture("right")
        glBegin(GL_QUADS)
        glColor(*self.get_color('right'))
        glNormal3f( 1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3d(0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture("right")
        # Top face
        self.get_texture("top")
        glBegin(GL_QUADS)
        glColor(*self.get_color('top'))
        glNormal3f( 0.0, 1.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3d(-0.5, 0.5, -0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(-0.5, 0.5, 0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(0.5, 0.5, 0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(0.5, 0.5, -0.5)
        glEnd()
        Textures.deactivate_texture("top")
        # Bottom face
        self.get_texture("bottom")
        glBegin(GL_QUADS)
        glColor(*self.get_color('bottom'))
        glNormal3f( 0.0, -1.0, 0.0)
        glTexCoord2f(0.0, 1.0); glVertex3d(0.5, -0.5, -0.5)
        glTexCoord2f(0.0, 0.0); glVertex3d(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0); glVertex3d(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0); glVertex3d(-0.5, -0.5, -0.5)
        glEnd()
        Textures.deactivate_texture("bottom")