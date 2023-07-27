from game_logic import GameLogic
from OpenGL.GL import *
from PIL import Image

class Textures:
    textures = {}

    @staticmethod
    def activate_texture(tag):
        if tag in Textures.textures:
            glBindTexture(GL_TEXTURE_2D, Textures.textures[tag])
            glEnable(GL_TEXTURE_2D)
        else:
            if tag not in GameLogic.files:
                return
            
            image = Image.open(GameLogic.files[tag])
            ix = image.size[0]
            iy = image.size[1]
            image = image.tobytes("raw", "RGBA", 0, -1)

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

            glEnable(GL_TEXTURE_2D)
            Textures.textures[tag] = texture_id

    @staticmethod
    def deactivate_texture(tag):
        glDisable(GL_TEXTURE_2D)