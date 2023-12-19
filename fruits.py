import pygame
vector=pygame.Vector2
from fruit_container import FruitContainer

class Fruits:
    def __init__(self):
        self.radius = 15
        self.color = "red"
        self.pos = vector((600, 00))
        self.vel = vector(0, 0)
        self.acc = vector(0, 0.45)
        self.friction = -0.12
        self.mouse_button_pressed = False
        self.current_time = pygame.time.get_ticks()
        self.collision_detected = False

        self.start_point = (675, 977)
        self.end_point = (1322, 977)
        self.line_width = 5
        self.fruit_container = FruitContainer()

    def update(self, event, screen):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_button_pressed = True

        if self.mouse_button_pressed:
            self.acc.x += self.vel.x * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
        else:
            self.moving_on_x_axis()

        self.container_collision()

    def moving_on_x_axis(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        interpolation_factor = 0.1
        self.pos.x += (mouse_x - self.pos.x) * interpolation_factor
        self.pos.y = 100

        self.pos.x = max(710, min(self.pos.x, 1272))

    def container_collision(self):
        fruit_rect = pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, 2 * self.radius, 2 * self.radius)
    
        fruit_container_rect = pygame.Rect(
            self.fruit_container.fruit_container_rect.x,
            self.fruit_container.fruit_container_rect.y,
            self.fruit_container.width,
            self.fruit_container.height
        )

        if fruit_rect.colliderect(fruit_container_rect) and fruit_rect.bottom >= fruit_container_rect.bottom:
            if self.vel.y > 0:
                self.vel.y = -self.vel.y / 2
                self.pos.y = min(fruit_rect.bottom, fruit_container_rect.bottom)

        if fruit_rect.colliderect(fruit_container_rect) and fruit_rect.right >= fruit_container_rect.left:
            if self.vel.x > 0:
                self.vel.x = -self.vel.x / 2
        
        if fruit_rect.colliderect(fruit_container_rect) and fruit_rect.left <= fruit_container_rect.right:
            if self.vel.x < 0:
                self.vel.x = -self.vel.x / 2
                
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)
        pygame.draw.line(screen, "black", self.start_point, self.end_point, self.line_width)