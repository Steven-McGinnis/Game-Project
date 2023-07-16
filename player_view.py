import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.setup()
        
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game_logic.set_property("quit", True)
                return
            
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  # type: ignore
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.display()

        pygame.display.flip()
        pygame.time.wait(10)

    def display(self):
        pass

    def new_game_object(self, game_object):
        pass

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
        gluPerspective(self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance)

        glEnable(GL_COLOR_MATERIAL)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
