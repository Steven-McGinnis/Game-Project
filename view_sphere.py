from view_object import ViewObject
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, pi

class SphereView(ViewObject):
    RADIUS = 1.0
    SLICES = 8
    STACKS = 8

    def draw(self):
        glPushMatrix()
        
        for i in range(self.SLICES):
            glBegin(GL_QUAD_STRIP)
            for j in range(self.STACKS+1):
                for k in range(2):
                    theta = (i+k) % self.SLICES / self.SLICES * 2 * pi
                    phi = j % self.STACKS / self.STACKS * pi
                    glColor3f(sin(theta), sin(phi), cos(theta)) # Set color for each vertex
                    x = cos(theta) * sin(phi) * self.RADIUS
                    y = sin(theta) * sin(phi) * self.RADIUS
                    z = cos(phi) * self.RADIUS
                    glVertex3f(x, y, z)
            glEnd()

        glPopMatrix()
