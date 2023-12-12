import os
import pygame
from config import image_folder

class FruitContainer:
    def __init__(self) -> None:
        
        self.fruit_container_path = os.path.join(image_folder, "fruit container.png")
        self.og_fruit_container = pygame.image.load(self.fruit_container_path)
        self.fruit_container = pygame.transform.scale(self.og_fruit_container, (672, 870.6))
        self.fruit_container_rect = self.og_fruit_container.get_rect()

        self.fruit_container_rect.x = 650
        self.fruit_container_rect.y = 132

    def update(self, screen):
        screen.blit(self.fruit_container, self.fruit_container_rect)
