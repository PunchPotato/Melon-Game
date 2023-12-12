import pygame
vector=pygame.Vector2

class Fruits:
    def __init__(self):
        self.radius = 15
        self.color = "red"
        self.pos = vector((600, 800))
        self.vel = vector(0, 0)
        self.acc = vector(0, 0.35)
        self.friction = - 0.12

    def update(self):
        self.acc.x += self.vel.x * self.friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Set the position of the ball to follow the mouse
                self.pos = pygame.mouse.get_pos()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)