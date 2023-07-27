from view_object import ViewObject
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from textures import Textures
from movies import Movies


class CubeViewColor(ViewObject):
    def get_color(self, face):
        if self.game_object.get_property('highlight_color') and self.game_object.highlight:
            return self.game_object.get_property('highlight_color')
        
        if face in self.game_object.faces:
            if self.game_object.faces[face]['type'] == 'color':
                return self.game_object.faces[face]['value']
            
        return [0.5, 0.5, 0.5, 1.0]
    
    def get_texture(self, face):
        if face in self.game_object.faces:
            if self.game_object.faces[face]['type'] == 'texture':
                Textures.activate_texture(self.game_object.faces[face]['value'])

            if self.game_object.faces[face]['type'] == 'movie':
                Movies.get_frame(self.game_object.faces[face]['value'])
    


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