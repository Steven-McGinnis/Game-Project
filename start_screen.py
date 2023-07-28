import pygame
import os

class StartScreen:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font_big = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

    def tick(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return False
                    if event.key == pygame.K_ESCAPE:
                        return True

            self.screen.fill((0,0,0))
            text_big = self.font_big.render('Zombie Survival', True, (255, 255, 255))
            self.screen.blit(text_big, (self.width/2 - text_big.get_width() // 2, self.height/3 - text_big.get_height() // 2))
            text_small = self.font_small.render('Press Enter to start', True, (255, 255, 255))
            self.screen.blit(text_small, (self.width/2 - text_small.get_width() // 2, self.height/2 - text_small.get_height() // 2))
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    start_screen = StartScreen()
    start_screen.tick()
    pygame.quit()
    os.system('python main.py')
