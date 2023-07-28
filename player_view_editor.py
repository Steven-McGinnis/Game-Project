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


class PlayerViewEditor:
    def __init__(self):
        # Variables
        # Initialize the Player
        self.player = None
        # Set Paused to False
        self.paused = False
        # Setup the Window
        self.setup()
        # Set the Distance for the Editor Cube Placement
        self.distance = 1.5
        # Set the Logger
        self.logger = Logger()
        # Set the Clock
        self.clock = pygame.time.Clock()
        # Set the Edit Mode to False
        self.edit_mode = False
        self.position_mode = False
        self.size_mode = False

        # Pause the Game
        GameLogic.set_property("paused", True)

        # Set the Camera Direction
        self.camera_direction = [0.0, 0.0, -1.0]
        
        # Create Dictionary to hold all rendered objects.
        self.view_objects = {}
        
        # Create a list to hold all the textures
        self.textures = []
        # Set the current texture to 0
        self.current_texture = 0

        # Subscribe to Events
        self.subscribe_to_events()

        # Create the HUD Variables
        self.hud = False
        if self.hud:
            self.create_hud_variables()

    def subscribe_to_events(self):
        pub.subscribe(self.new_game_object, "create")
        pub.subscribe(self.delete_game_object, "delete")
        pub.subscribe(self.addAmmo, "ammo")
        pub.subscribe(self.deleteAll, "delete_all")
    
    # Clears out all the View Objects for the Level
    def deleteAll(self):
        self.view_objects = {}

    def delete_game_object(self, game_object):
        if game_object.id in self.view_objects:
            del self.view_objects[game_object.id]



    def create_hud_variables(self):
        self.health = 100
        self.stamina = 100
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
            _("Stamina: ") + str(self.stamina), True, (0, 0, 255), (0, 0, 0, 0)
        )
        self.update_texture(img, self.stamina_texture)

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

        self.window_width = 1920
        self.window_height = 1080
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


    def find_textures(self):
        self.textures = []

        for file in GameLogic.files:
            if GameLogic.files[file].startswith("./textures/"):
                self.textures.append(file)


    def tick(self):
        if not self.textures:
            self.find_textures()

        mouseMove = (0, 0)
        clicked = False

        self.apply_texture = False
        self.clear_texture = False

        self.position_adjust = 0.0
        self.size_adjust = 0.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                GameLogic.set_property("quit", True)
                return


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

                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    Localize.save()
                    GameLogic.save_world()

                if event.key == pygame.K_e:
                    self.edit_mode = not self.edit_mode

                if event.key == pygame.K_t:
                    self.current_texture = (self.current_texture + 1) % len(self.textures)
                    self.logger.add_log(_("Texture: ") + self.textures[self.current_texture])

                if event.key == pygame.K_r:
                    self.apply_texture = True

                if event.key == pygame.K_z:
                    self.clear_texture = True

                if event.key == pygame.K_f:
                    self.position_mode = not self.position_mode

                if event.key == pygame.K_c:
                    self.size_mode = not self.size_mode


            if not self.paused:
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - self.viewCenter[i] for i in range(2)]
                pygame.mouse.set_pos(self.viewCenter)

                if event.type == pygame.MOUSEWHEEL:
                    if self.edit_mode:
                        self.distance = max(1.5, self.distance+event.y)

                    if self.position_mode:
                        self.position_adjust = event.y * 0.1

                    if self.size_mode:
                        self.size_adjust = event.y * 0.1

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True

                    if self.edit_mode:
                        self.create_object()

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

            if self.hud:
                if keypress[pygame.K_LSHIFT]:
                    self.use_stamina(1)

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

                camera_direction = numpy.linalg.inv(self.viewMatrix)
                camera_direction = camera_direction[2][0:3]
                camera_direction[0] *= -1
                camera_direction[1] *= -1
                camera_direction[2] *= -1
                self.camera_direction = camera_direction

            if self.hud:
                if keypress[pygame.K_LSHIFT] == False and self.stamina < 100:
                    self.recover_stamina(1)


            self.enable_lighting()

            glClearColor(0.53, 0.81, 0.92, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # type: ignore
            glPushMatrix()

            self.display()
            glPopMatrix()
            self.draw_guide()


            self.disable_lighting()

            self.render_hud()

            pygame.display.flip()
            self.clock.tick(60)

    def draw_guide(self):
        if not self.edit_mode:
            return
    
        camera_direction = numpy.array(self.camera_direction)
        current = numpy.array(self.player.position) # type: ignore
        
        position = (current + self.distance * camera_direction).tolist()

        position[0] = round(position[0])
        position[1] = round(position[1])
        position[2] = round(position[2])

        glPushMatrix()
        glTranslate(*position)  

        glBegin(GL_QUADS)
        glColor(0.25, 0.25, 0.25, 0.5)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, 0.5, 0.5)
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3d(-0.5, 0.5, -0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(-0.5, 0.5, 0.5)
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3d(0.5, 0.5, -0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(-0.5, 0.5, -0.5)
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(0.5, 0.5, -0.5)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3d(-0.5, 0.5, -0.5)
        glVertex3d(-0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, 0.5)
        glVertex3d(0.5, 0.5, -0.5)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3d(-0.5, -0.5, 0.5)
        glVertex3d(-0.5, -0.5, -0.5)
        glVertex3d(0.5, -0.5, -0.5)
        glVertex3d(0.5, -0.5, 0.5)
        glEnd()

        glPopMatrix()
        


    def create_object(self):
        camera_direction = numpy.array(self.camera_direction)
        current = numpy.array(self.player.position) # type: ignore

        position = (current + self.distance * camera_direction).tolist()
        position[0] = round(position[0])
        position[1] = round(position[1])
        position[2] = round(position[2])

        GameLogic.create_object({"kind": "cube2", "position": position})

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
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def handle_mouse(self, pos, clicked):
        windowX = pos[0]
        windowY = self.window_height - pos[1]

        glSelectBuffer(200)
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
            
            if self.apply_texture:
                for face in self.get_faces(closest):
                    closest.faces[face] = {'type': 'texture', 'value': self.textures[self.current_texture]}

            if self.clear_texture:
                for face in self.get_faces(closest):
                    del closest.faces[face]

            if self.position_mode and self.position_adjust:
                for face in self.get_faces(closest):
                    if face == 'front':
                        closest.position[2] += self.position_adjust
                    if face == 'back':
                        closest.position[2] -= self.position_adjust
                    if face == 'left':
                        closest.position[0] += self.position_adjust
                    if face == 'right':
                        closest.position[0] -= self.position_adjust
                    if face == 'top':
                        closest.position[1] -= self.position_adjust
                    if face == 'bottom':
                        closest.position[1] += self.position_adjust

            if self.size_mode and self.size_adjust:
                pass

            if clicked:
                closest.clicked(self.player)
                if self.hud:
                    self.shoot()
                if closest.identifier:
                    self.logger.add_log(_("Object clicked: ") + closest.identifier)
        

    def get_faces(self, game_object):
        camera_direction = numpy.array(self.camera_direction)
        current = numpy.array(self.player.position) # type: ignore

        mypos = current + 1.5 * camera_direction

        otherpos = numpy.array(game_object.position)
        distance = numpy.linalg.norm(mypos - otherpos)
        direction_vector = (mypos - otherpos) / distance

        max_direaction = max(direction_vector, key=abs)
        indices = [i for i, j in enumerate(direction_vector) if j == max_direaction]

        results = []

        for index in indices:
            if index == 0 and direction_vector[index] < 0:
                results.append("left")

            if index == 0 and direction_vector[index] > 0:
                results.append("right")

            if index == 1 and direction_vector[index] < 0:
                results.append("bottom")

            if index == 1 and direction_vector[index] > 0:
                results.append("top")

            if index == 2 and direction_vector[index] < 0:
                results.append("front")
            
            if index == 2 and direction_vector[index] > 0:
                results.append("back")
            
        return results


    # Sets the Modes and Renders the HUD
    def render_hud(self):
        glDisable(GL_DEPTH_TEST)
        glDepthMask(GL_FALSE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window_width, 0, self.window_height)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if self.hud:
            self.render_health_stamina()  # Call the new function here

        self.render_log()

        glDisable(GL_BLEND)

        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
        

    def render_health_stamina(self):
        glEnable(GL_TEXTURE_2D)

        # Render Health
        glBindTexture(GL_TEXTURE_2D, self.health_texture)
        self.render_text_quad(10, self.window_height - 40)

        # Render Stamina
        glBindTexture(GL_TEXTURE_2D, self.stamina_texture)
        self.render_text_quad(10, self.window_height - 80)

        # Render Ammo
        glBindTexture(GL_TEXTURE_2D, self.ammo_texture)
        self.render_text_quad(10, self.window_height - 120)
        

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
            img = pygame.font.SysFont("Arial", 30).render(
                log_entry, True, (255, 255, 255)  # Use white color
            )
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
            glVertex2f(self.window_width - 200, y)  # Move 50 pixels to the left
            glTexCoord2f(1.0, 1.0)
            glVertex2f(self.window_width - 50, y)  # Move 50 pixels to the left
            glTexCoord2f(1.0, 0.0)
            glVertex2f(self.window_width - 50, y - 30)
            glTexCoord2f(0.0, 0.0)
            glVertex2f(self.window_width - 200, y - 30)
            glEnd()

            glDeleteTextures([texture])  # Delete the texture after using it
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)

            y -= 30  # Move up for the next entry



    def take_damage(self, amount):
        self.health -= amount
        self.update_health_stamina_textures()

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
        self.ammo += 21
        self.update_health_stamina_textures()

    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            self.update_health_stamina_textures()