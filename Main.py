import os
import pygame
import sys
from fruit_container import FruitContainer
from config import image_folder
from fruits import Fruits

class MelonGame:
    def __init__(self):
        pygame.init()

        self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Melon Game")

        self.background_path = os.path.join(image_folder, "suika game background.png")
        self.background = pygame.image.load(self.background_path)
        self.background_rect = self.background.get_rect()

        self.fruit_container = FruitContainer() 
        self.fruits = Fruits()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
            self.fruits.update(event)

            self.screen.blit(self.background, self.background_rect)
            self.fruit_container.update(self.screen)
            self.fruits.draw(self.screen)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def quit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MelonGame()
    game.run()