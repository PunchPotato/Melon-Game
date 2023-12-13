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
            self.mouse_button_pressed = True
        
        if self.mouse_button_pressed == True:
            self.acc.x += self.vel.x * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
        elif self.mouse_button_pressed == False:
            self.moving_on_x_axis()

    def moving_on_x_axis(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.pos.x += (mouse_x - self.pos.x) * 0.1
        self.pos.y = 100
        
        if self.pos.x <= 730: 
            self.pos.x = 730
        elif self.pos.x >= 1252:
            self.pos.x = 1252


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)