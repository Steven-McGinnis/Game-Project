# end_screen.py
import pygame
import sys
from localize import _

class EndScreen:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font_big = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

    def display(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0,0,0))
            game_over_text = self.font_big.render(_('Game Over'), True, (255, 255, 255))
            self.screen.blit(game_over_text, (self.width/2 - game_over_text.get_width() // 2, self.height/3 - game_over_text.get_height() // 2))
            thanks_text = self.font_small.render(_('Thank you for playing'), True, (255, 255, 255))
            self.screen.blit(thanks_text, (self.width/2 - thanks_text.get_width() // 2, self.height/2 - thanks_text.get_height() // 2))

            pygame.display.flip()
            self.clock.tick(30)
