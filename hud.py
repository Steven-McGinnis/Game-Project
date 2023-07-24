import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class HUD:
    def __init__(self, game_logic, window_width, window_height):
        self.game_logic = game_logic
        self.window_width = window_width
        self.window_height = window_height
        self.create_hud_variables()

    def create_hud_variables(self):
        self.health = 100
        self.stamina = 100
        self.clicks = 0
        self.health_texture = glGenTextures(1)
        self.stamina_texture = glGenTextures(1)
        self.clicks_texture = glGenTextures(1)
        self.update_health_stamina_textures()

    def update_health_stamina_textures(self):
        img_health = pygame.font.SysFont("Arial", 25).render(str(self.health), True, (255, 0, 0), (0, 0, 0, 0))
        img_stamina = pygame.font.SysFont("Arial", 25).render(str(self.stamina), True, (0, 255, 0), (0, 0, 0, 0))
        self.update_texture(img_health, self.health_texture)
        self.update_texture(img_stamina, self.stamina_texture)
        self.update_clicks_texture()

    def update_texture(self, img, texture):
        ix, iy, image = img.get_width(), img.get_height(), pygame.image.tostring(img, "RGBA", 1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

    def update_clicks_texture(self):
        img = pygame.font.SysFont("Arial", 25).render("Clicks :" + str(self.clicks), True, (0, 255, 0), (0, 0, 0, 0))
        self.update_texture(img, self.clicks_texture)
    
    def user_clicked(self):
        self.clicks += 1
        self.update_clicks_texture()

    def render_hud(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.render_health_stamina()
        self.render_clicks()

    def render_health_stamina(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.health_texture)
        self.render_text_quad(self.window_width - 200, 100)
        glBindTexture(GL_TEXTURE_2D, self.stamina_texture)
        self.render_text_quad(self.window_width - 200, 120)
        glDisable(GL_TEXTURE_2D)

    def render_clicks(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.clicks_texture)
        self.render_text_quad(self.window_width - 200, 140)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
    
    def render_text_quad(self, x, y):
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + 100, y)
        glTexCoord2f(1, 1); glVertex2f(x + 100, y + 25)
        glTexCoord2f(0, 1); glVertex2f(x, y + 25)
        glEnd()
