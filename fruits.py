import pygame
vector=pygame.Vector2

class Fruits:
    def __init__(self):
        self.radius = 15
        self.color = "red"
        self.pos = vector((600, 00))
        self.vel = vector(0, 0)
        self.acc = vector(0, 0.35)
        self.friction = - 0.12
        self.mouse_button_pressed = False

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button pressed")
            self.mouse_button_pressed = True
        else:
            print("Mouse button released")
        
        if self.mouse_button_pressed == True:
            self.acc.x += self.vel.x * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)