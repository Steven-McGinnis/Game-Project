from OpenGL.GL import * # type: ignore
from OpenGL.GLU import * # type: ignore
from pubsub import pub
from pygame.locals import * # type: ignore
from view_cube import CubeView
from view_sphere import SphereView
from view_cube2 import CubeViewColor
from view_billboard_cube import BillboardCubeView
from localize import _
from localize import Localize
import numpy
import pygame
from game_logic import GameLogic
from view_world import WorldView
from logger import Logger
import time
from sounds import Sounds


class PlayerView:
    def __init__(self):
        self.player = None
        self.paused = False
        self.setup()
        self.logger = Logger()
        self.clock = pygame.time.Clock()
        
        self.view_objects = {}
        
        self.subscribe_to_events()
        self.create_hud_variables()
        self.last_ammo_update = 0  # initialize the last update time to 0
        self.cooldown_period = 1  # cooldown period in seconds (set as needed)
        self.last_health_update = 0  # initialize the last update time to 0
        self.health_cooldown_period = 1  # cooldown period in seconds (set as needed)

    def subscribe_to_events(self):
        pub.subscribe(self.new_game_object, "create")
        pub.subscribe(self.delete_game_object, "delete")
        pub.subscribe(self.addAmmo, "ammo")
        pub.subscribe(self.deleteAll, "delete_all")
        pub.subscribe(self.display_round_wait_timer, "round_wait")
        pub.subscribe(self.take_damage, "take_damage2")
    
    # Clears out all the View Objects for the Level
    def deleteAll(self):
        self.view_objects = {}

    def delete_game_object(self, game_object):
        if game_object.id in self.view_objects:
            del self.view_objects[game_object.id]



    def create_hud_variables(self):
        self.health = 100
        self.ammo = 20
        self.health_texture = glGenTextures(1)
        self.stamina_texture = glGenTextures(1)
        self.ammo_texture = glGenTextures(1)
        self.update_health_stamina_textures()

    def update_health_stamina_textures(self):
        img = pygame.font.SysFont("Arial", 25).render(
            _("Health: ") + str(self.health), True, (255, 0, 0), (0, 0, 0, 0)
        )
        self.update_texture(img, self.health_texture)

        img = pygame.font.SysFont("Arial", 25).render(
            _("Ammo: ") + str(self.ammo), True, (0, 255, 0), (0, 0, 0, 0)
        )
        self.update_texture(img, self.ammo_texture)

    def update_texture(self, img, texture):
        w, h = img.get_size()
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)  # type: ignore
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data
        )

    # Setup the Window
    def setup(self):
        pygame.init()

        self.window_width = 1024    
        self.window_height = 768
        self.viewCenter = (self.window_width // 2, self.window_height // 2)

        pygame.display.set_mode(
            (self.window_width, self.window_height), DOUBLEBUF | OPENGL
        )

        self.field_of_view = 60
        self.aspect_ratio = self.window_width / self.window_height
        self.near_distance = 0.1
        self.far_distance = 100.0

        self.prepare_3d()
        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    def tick(self):
        if self.health <= 0:
            pygame.quit()
            GameLogic.set_property("quit", True)
            return
        mouseMove = (0, 0)
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                GameLogic.set_property("quit", True)
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                self.shoot()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    GameLogic.set_property("quit", True)
                    return

                if event.key == pygame.K_SPACE:
                    pub.sendMessage("key-jump")

                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    GameLogic.set_property("paused", self.paused)
                    pygame.mouse.set_pos(self.viewCenter)

                if event.key == pygame.K_l:
                    Localize.switch_language()

            if not self.paused:
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - self.viewCenter[i] for i in range(2)]
                pygame.mouse.set_pos(self.viewCenter)

        # If Not Paused Do This
        if not self.paused:
            pos = pygame.mouse.get_pos()
            self.handle_mouse(pos, clicked)
            self.prepare_3d()

            keypress = pygame.key.get_pressed()
            if keypress[pygame.K_w]:
                pub.sendMessage("key-w")

            if keypress[pygame.K_s]:
                pub.sendMessage("key-s")

            if keypress[pygame.K_a]:
                pub.sendMessage("key-a")

            if keypress[pygame.K_d]:
                pub.sendMessage("key-d")

            pub.sendMessage("rotate-y", amount=mouseMove[0])
            pub.sendMessage("rotate-x", amount=mouseMove[1])

            if self.player:
                glRotate(self.player.x_rotation, 1.0, 0.0, 0.0)
                glRotate(self.player.y_rotation, 0.0, 1.0, 0.0)
                glTranslate(
                    -self.player.position[0],
                    -self.player.position[1],
                    -self.player.position[2],
                )
                self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            self.enable_lighting()

            glClearColor(0.53, 0.81, 0.92, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # type: ignore
            glPushMatrix()

            self.display()
            glPopMatrix()

            self.disable_lighting()

            self.render_hud()

            pygame.display.flip()
            self.clock.tick(60)

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

        if game_object.kind == "billboard_cube":
            self.view_objects[game_object.id] = BillboardCubeView(game_object)

        if game_object.kind == "player":
            self.player = game_object

        if game_object.kind == 'world':
            self.view_objects[game_object.id] = WorldView(game_object)

        if game_object.kind == 'cube2':
            self.view_objects[game_object.id] = CubeViewColor(game_object)

    def prepare_3d(self):
        glViewport(0, 0, self.window_width, self.window_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(
            self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance
        )
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_COLOR_MATERIAL)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

    def handle_mouse(self, pos, clicked):
        windowX = pos[0]
        windowY = self.window_height - pos[1]

        glSelectBuffer(100)
        glRenderMode(GL_SELECT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        gluPickMatrix(windowX, windowY, 20, 20, glGetIntegerv(GL_VIEWPORT))
        gluPerspective(
            self.field_of_view, self.aspect_ratio, self.near_distance, self.far_distance
        )

        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(self.viewMatrix)
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

            if not closest or numpy.linalg.norm(obj_pos - camera) < numpy.linalg.norm(
                closest.position - camera
            ):
                closest = self.view_objects[id].game_object

        if closest is None:
            print(_("No closest object found"))
            return

        if closest:
            closest.hover(self.player)
            if clicked:
                if closest.identifier and closest.identifier.startswith("enemy"):
                    if self.ammo <= 0:
                        self.logger.add_log(_("No Ammo!"))
                    else:
                        closest.clicked(self.player)
                        if closest.identifier:
                            self.logger.add_log(_("Enemy Hit: ") + closest.identifier)
                elif closest.identifier:
                    closest.clicked(self.player)
                    if closest.identifier:
                        self.logger.add_log(_("Object clicked: ") + closest.identifier)






    def render_hud(self):
        glDisable(GL_DEPTH_TEST)
        glDepthMask(GL_FALSE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window_width, 0, self.window_height)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.render_health_stamina()  # Call the new function here
        self.display_round_wait_timer(GameLogic.round_timer, GameLogic.game_state)

        self.render_log()

        glDisable(GL_BLEND)

        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
        

    def render_health_stamina(self):
        glEnable(GL_TEXTURE_2D)

        # Render Health
        glBindTexture(GL_TEXTURE_2D, self.health_texture)
        self.render_text_quad(10, self.window_height - 40)

        # Render Ammo
        glBindTexture(GL_TEXTURE_2D, self.ammo_texture)
        self.render_text_quad(10, self.window_height - 80)
        

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

    def render_text_quad(self, x, y):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 1.0)  # White color
        glTexCoord2f(0.0, 1.0)
        glVertex2f(x, y + 30)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(x + 200, y + 30)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(x + 200, y)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(x, y)
        glEnd()

    # Turn Lighting On
    def enable_lighting(self):
        light_ambient = [0.2, 0.2, 0.2, 1.0]
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        light_position = [0.0, 4.0, 1.0, 1.0]

        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

    # Turn Lighting Off
    def disable_lighting(self):
        glDisable(GL_LIGHTING)

    def render_log(self):
        # Display the click log
        y = self.window_height  # Adjust this as needed
        for log_entry in self.logger.get_log():
            img = pygame.font.SysFont("Arial", 20).render(
                log_entry, True, (128, 128, 128)
            )  # Use gray color
            w, h = img.get_size()
            data = pygame.image.tostring(img, "RGBA", 1)  # type: ignore
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexImage2D(
                GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data
            )

            glEnable(GL_TEXTURE_2D)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            glBegin(GL_QUADS)
            glColor4f(1.0, 1.0, 1.0, 1.0)  # White color to keep texture color
            glTexCoord2f(0.0, 1.0)
            glVertex2f(self.window_width - 100, y)  # Reduce width here
            glTexCoord2f(1.0, 1.0)
            glVertex2f(self.window_width, y)
            glTexCoord2f(1.0, 0.0)
            glVertex2f(self.window_width, y - 20)
            glTexCoord2f(0.0, 0.0)
            glVertex2f(self.window_width - 100, y - 20)  # And here
            glEnd()

            glDeleteTextures([texture])  # Delete the texture after using it
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)

            y -= 20  # Move up for the next entry

    def take_damage(self):
        current_time = time.time()
        if current_time - self.last_health_update >= self.health_cooldown_period:
            self.health -= 25
            self.update_health_stamina_textures()
            self.last_health_update = current_time

    def heal(self, amount):
        self.health += amount
        self.update_health_stamina_textures()

    def use_stamina(self, amount):
        if self.stamina > 0: 
            self.stamina -= amount
            self.update_health_stamina_textures()

    def recover_stamina(self, amount):
        if self.stamina < 100:
            self.stamina += amount
            self.update_health_stamina_textures()

        if self.stamina > 100:
            self.stamina = 100

    def addAmmo(self):
        current_time = time.time()  # get the current time

        # check if the cooldown period has passed
        if current_time - self.last_ammo_update < self.cooldown_period:
            return

        self.ammo += 10
        Sounds.play_sound("reload")
        self.update_health_stamina_textures()
        self.last_ammo_update = current_time

    def shoot(self):
        if self.ammo > 0:
            Sounds.play_sound("shoot")
            self.ammo -= 1
            self.update_health_stamina_textures()
        else:
            Sounds.play_sound("empty")

    def display_round_wait_timer(self, timer, game_state):
        if game_state == "round_wait":
            mode = "Round Begins in {:.2f} seconds".format(timer)

        elif game_state == "round_end":
            mode = "Round " + str(timer) + " Complete!"

        else:
            mode = "Survive the Round!"



        y = self.window_height - 30  # Adjust the starting position

        img = pygame.font.SysFont("Arial", 40).render(
            mode, True, (255, 0, 0)  # Use white color
        )
        w, h = img.get_size()

        # Center the text
        x = (self.window_width - w) // 2

        img = pygame.transform.flip(img, False, True)  # Flip the image
        data = pygame.image.tostring(img, "RGBA", 1)  # type: ignore
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data
        )

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBegin(GL_QUADS)
        glColor4f(1.0, 1.0, 1.0, 1.0)  # White color to keep texture color
        glTexCoord2f(0.0, 0.0)
        glVertex2f(x, y)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(x + w, y)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(x + w, y - h)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(x, y - h)
        glEnd()

        glDeleteTextures([texture])  # Delete the texture after using it
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
