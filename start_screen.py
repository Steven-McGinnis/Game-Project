# start_screen.py
import pygame
import sys
from localize import _

class StartScreen:
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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.screen.fill((0,0,0))
            title_text = self.font_big.render(_('Zombie Survival'), True, (255, 255, 255))
            self.screen.blit(title_text, (self.width/2 - title_text.get_width() // 2, self.height/3 - title_text.get_height() // 2))
            start_text = self.font_small.render(_('Press Enter to start'), True, (255, 255, 255))
            self.screen.blit(start_text, (self.width/2 - start_text.get_width() // 2, self.height/2 - start_text.get_height() // 2))

            pygame.display.flip()
            self.clock.tick(30)
