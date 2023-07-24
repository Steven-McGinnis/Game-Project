from OpenGL.GL import *
from OpenGL.GLU import *
from pubsub import pub
from pygame.locals import *
from view_cube import CubeView
from view_floor import FloorView
from view_sphere import SphereView
from view_billboard_cube import BillboardCubeView
from localize import _
import numpy
import pygame
import random

class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.view_objects = {}
        
        pub.subscribe(self.new_game_object, "create")

        self.paused = False
        self.camera_angle = 0.0

        self.setup()
        global clicks_texture
        global clicks
        clicks = -1
        clicks_texture = glGenTextures(1)
        self.user_clicked();

    
    # Setup the Window
    def setup(self):
        pygame.init()

        self.window_width = 800
        self.window_height = 600
        self.viewCenter = (self.window_width // 2, self.window_height // 2)

        pygame.display.set_mode((self.window_width, self.window_height), DOUBLEBUF|OPENGL)

        self.field_of_view = 60
        self.aspect_ratio = self.window_width / self.window_height
        self.near_distance = 0.1
        self.far_distance = 100.0
        
        self.prepare_3d()
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    def user_clicked(self):
        global clicks
        global clicks_texture
        clicks += 1
        img = pygame.font.SysFont("Arial", 25).render(_("Clicks: ")+str(clicks), True, (0, 255, 0), (0, 0, 0, 0))


        w, h = img.get_size()
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, clicks_texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)  # type: ignore
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    
    def tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.game_logic.set_property("quit", True)
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.handle_click(pos)
                self.user_clicked()

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

                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    pygame.mouse.set_pos(self.viewCenter)

        # If Not Paused Do This
        if not self.paused:
            self.prepare_3d()

            keypress = pygame.key.get_pressed()

            glPushMatrix()
            glLoadIdentity()
            
            if keypress[pygame.K_w]:
                glTranslatef(0, 0, 0.1)
            if keypress[pygame.K_s]:
                glTranslatef(0, 0, -0.1)
            if keypress[pygame.K_a]:
                glTranslatef(0.1, 0, 0)
            if keypress[pygame.K_d]:
                glTranslatef(-0.1, 0, 0)

            glMultMatrixf(self.viewMatrix)
            self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            glPopMatrix()
            glMultMatrixf(self.viewMatrix)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) 
            glPushMatrix()

            self.display()
            glPopMatrix()

            self.render_hud()

            pygame.display.flip()
            pygame.time.wait(10)

    # Display All Objects in Scene
    def display(self):
        glInitNames()

        for id in self.view_objects:
            self.view_objects[id].display()

    # Call the Right Classes to Display the Right Objects
    def new_game_object(self, game_object):
        if game_object.kind == "cube":
            self.view_objects[game_object.id] = CubeView(game_object)

        if game_object.kind == "sphere":
            self.view_objects[game_object.id] = SphereView(game_object)

        if game_object.kind == "floor":
            texture_file = "./textures/grassSeamless.png"  # Replace with the path to your texture file
            self.view_objects[game_object.id] = FloorView(game_object, texture_file)

        if game_object.kind == "billboard_cube":
            self.view_objects[game_object.id] = BillboardCubeView(game_object)

    

    def prepare_3d(self):
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

        glSelectBuffer(100)
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

            if not closest or numpy.linalg.norm(obj_pos - camera) < numpy.linalg.norm(closest.position - camera):
                closest = self.view_objects[id].game_object

        if closest is None:
            print("No closest object found")
            return

        closest.clicked()

    def render_hud(self):
        glDisable(GL_DEPTH_TEST)
        glDepthMask(GL_FALSE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window_width, 0, self.window_height)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, clicks_texture)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glClearColor(0.0, 0.0, 0.0, 1.0)

        glBegin(GL_QUADS)
        glColor4f(0.0, 1.0, 0.0, 1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(0, self.window_height)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(200, self.window_height)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(200, self.window_height - 50)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(0, self.window_height - 50)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        glDisable(GL_BLEND)

        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
