import pygame
vector=pygame.Vector2


class Fruit:
    def __init__(self, x, y, speed, horizontal_speed, color, radius, is_dropping):
        self.x = x
        self.y = y
        self.speed = speed
        self.horizontal_speed = horizontal_speed
        self.color = color
        self.radius = radius
        self.is_dropping = is_dropping