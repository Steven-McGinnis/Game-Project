from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from localize import _

class Hud:
    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.health = 100
        self.stamina = 100
        self.ammo = 20
        self.health_texture = glGenTextures(1)
        self.stamina_texture = glGenTextures(1)
        self.ammo_texture = glGenTextures(1)
        self.update_hud_textures()

    def update_hud_textures(self):
        self.update_texture(
            _("Health: ") + str(self.health), 
            self.health_texture,
            color=(255, 0, 0)
        )
        self.update_texture(
            _("Stamina: ") + str(self.stamina), 
            self.stamina_texture,
            color=(0, 0, 255)
        )
        self.update_texture(
            _("Ammo: ") + str(self.ammo),
            self.ammo_texture,
            color=(0, 255, 0)
        )

    def update_texture(self, text, texture, color=(255, 255, 255)):
        img = pygame.font.SysFont("Arial", 25).render(
            text, True, color, (0, 0, 0, 0)
        )
        w, h = img.get_size()
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        data = pygame.image.tostring(img, "RGBA", 1)  # type: ignore
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data
        )

    def render_hud(self):
        glDisable(GL_DEPTH_TEST)
        glDepthMask(GL_FALSE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window_width, 0, self.window_height)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.render_hud_elements()

        glDisable(GL_BLEND)

        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)
        
    def render_hud_elements(self):
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

    def useStamina(self, amount):
        self.stamina = max(0, self.stamina - amount)
        self.update_hud_textures()

    def restoreStamina(self, amount):
        self.stamina = min(100, self.stamina + amount)
        self.update_hud_textures()