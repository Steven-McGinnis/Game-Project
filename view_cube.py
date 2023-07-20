from view_object import ViewObject
from OpenGL.GL import *
from OpenGL.GLU import *

class CubeView(ViewObject):
    def draw(self):
        glBegin(GL_QUADS)
        # Front face
        glColor(1.0, 0.0, 0.0, 1.0)
        glNormal3f( 0.0, 0.0, 1.0)
        glVertex3d(-1.0, 1.0, 1.0)
        glVertex3d(-1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, 1.0)
        glVertex3d(1.0, 1.0, 1.0)
        # Left face
        glColor(0.0, 1.0, 0.0, 1.0)
        glNormal3f( -1.0, 0.0, 0.0)
        glVertex3d(-1.0, 1.0, 1.0)
        glVertex3d(-1.0, -1.0, 1.0)
        glVertex3d(-1.0, -1.0, -1.0)
        glVertex3d(-1.0, 1.0, -1.0)
        # Back face
        glColor(0.0, 0.0, 1.0, 1.0)
        glNormal3f( 0.0, 0.0, -1.0)
        glVertex3d(-1.0, 1.0, -1.0)
        glVertex3d(-1.0, -1.0, -1.0)
        glVertex3d(1.0, -1.0, -1.0)
        glVertex3d(1.0, 1.0, -1.0)
        # Right face
        glColor(1.0, 1.0, 0.0, 1.0)
        glNormal3f( 1.0, 0.0, 0.0)
        glVertex3d(1.0, 1.0, 1.0)
        glVertex3d(1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, -1.0)
        glVertex3d(1.0, 1.0, -1.0)
        # Top face
        glColor(0.0, 1.0, 1.0, 1.0)
        glNormal3f( 0.0, 1.0, 0.0)
        glVertex3d(-1.0, 1.0, 1.0)
        glVertex3d(1.0, 1.0, 1.0)
        glVertex3d(1.0, 1.0, -1.0)
        glVertex3d(-1.0, 1.0, -1.0)
        # Bottom face
        glColor(1.0, 1.0, 1.0, 1.0)
        glNormal3f( 0.0, -1.0, 0.0)
        glVertex3d(-1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, 1.0)
        glVertex3d(1.0, -1.0, -1.0)
        glVertex3d(-1.0, -1.0, -1.0)
        glEnd()