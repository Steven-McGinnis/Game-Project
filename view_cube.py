from view_object import ViewObject
from OpenGL.GL import *
from OpenGL.GLU import *


class CubeView(ViewObject):
    def draw(self):
        glBegin(GL_QUADS)
        # Front face
        glColor(1.0, 0.0, 0.0, 1.0)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, 0.5, 0.5)
        # Left face
        glColor(0.0, 1.0, 0.0, 1.0)
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        # Back face
        glColor(0.0, 0.0, 1.0, 1.0)
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3d(-0.5, 0.5, -0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(0.5, 0.5, -0.5)
        # Right face
        glColor(1.0, 1.0, 0.0, 1.0)
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(0.5, 0.5, -0.5)
        # Top face
        glColor(0.0, 1.0, 1.0, 1.0)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        # Bottom face
        glColor(1.0, 1.0, 1.0, 1.0)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glEnd()
