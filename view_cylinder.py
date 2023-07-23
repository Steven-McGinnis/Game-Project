from OpenGL.GL import *
from OpenGL.GLU import *
from view_object import ViewObject

class CylinderView(ViewObject):
    BASE_RADIUS = 1.0
    TOP_RADIUS = 1.0
    HEIGHT = 2.0
    SLICES = 50
    STACKS = 50

    def draw(self):
        glPushMatrix()
        glColor(1.0, 1.0, 1.0, 1.0) # Set the color to white
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH) # Create smooth normals
        gluCylinder(quadric, self.BASE_RADIUS, self.TOP_RADIUS, self.HEIGHT, self.SLICES, self.STACKS)
        gluDeleteQuadric(quadric) # Delete the quadric
        glPopMatrix()
