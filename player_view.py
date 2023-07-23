import pygame
from pubsub import pub
from view_cube import CubeView
from view_sphere import SphereView
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import numpy

class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.view_objects = {}

        pub.subscribe(self.new_game_object, "create")

        self.setup()
        
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game_logic.set_property("quit", True)
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handle_click(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    self.game_logic.set_property("quit", True)
                    return
                
                if event.key == pygame.K_SPACE:
                    x = random.uniform(-10, 10)  # Generate a random number between -10 and 10
                    y = random.uniform(-10, 10)
                    z = random.uniform(-10, 10)
                    self.game_logic.create_object("sphere", [x, y, -10], "rotating")
            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # type: ignore
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.display()

        pygame.display.flip()
        pygame.time.wait(10)

    def display(self):
        glInitNames()

        for id in self.view_objects:
            self.view_objects[id].display()

    def new_game_object(self, game_object):
        if game_object.kind == "cube":
            self.view_objects[game_object.id] = CubeView(game_object)

        if game_object.kind == "sphere":
            self.view_objects[game_object.id] = SphereView(game_object) 

    def setup(self):
        pygame.init()

        self.window_width = 800
        self.window_height = 600

        pygame.display.set_mode((self.window_width, self.window_height), DOUBLEBUF|OPENGL)

        self.field_of_view = 60
        self.aspect_ratio = self.window_width / self.window_height
        self.near_distance = 0.1
        self.far_distance = 100.0


        self.reset_opengl()

    def reset_opengl(self):
        glViewport(0, 0, self.window_width, self.window_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_COLOR_MATERIAL)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

    def handle_click(self, pos):
        windowX = pos[0]
        windowY = self.window_height - pos[1]

        glSelectBuffer(20)
        glRenderMode(GL_SELECT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        gluPickMatrix(windowX, windowY, 20, 20, glGetIntegerv(GL_VIEWPORT))
        gluPerspective(self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance)

        glMatrixMode(GL_MODELVIEW)
        self.display()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        buffer = glRenderMode(GL_RENDER)

        if buffer is None:
            print("Buffer is None")
            return

        objects = []
        for record in buffer:
            min_depth, max_depth, name = record
            objects += name

        if not objects:
            return
        
        camera = numpy.linalg.inv(glGetFloatv(GL_MODELVIEW_MATRIX))
        camera = camera[3][0:3]

        closest = None

        for id in objects:
            obj_pos = self.view_objects[id].game_object.position

            if not closest or numpy.linalg.norm(obj_pos - camera) < numpy.linalg.norm(closest - camera):
                closest = self.view_objects[id].game_object

        if closest is None:
            print("No closest object found")
            return

        closest.clicked()
