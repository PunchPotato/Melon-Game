import random
import pygame
vector=pygame.Vector2
from fruit_container import FruitContainer

class Fruits:
    def __init__(self, initial_position):
        self.radius = 15
        self.color = "red"
        self.pos = vector(initial_position)
        self.vel = vector(0, 0)
        self.acc = vector(0, 0.45)
        self.friction = -0.12
        self.mouse_button_pressed = False
        self.current_time = pygame.time.get_ticks()
        self.collision_detected = False
        self.fruits_list = []
        self.radius = random.randint(10, 30)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.follow_mouse = False

        self.start_point = (675, 977)
        self.end_point = (1322, 977)
        self.line_width = 5
        self.fruit_container = FruitContainer()

    def update(self, event, screen):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_button_pressed = True

        if self.mouse_button_pressed:
            for fruit in self.fruits_list[:-1]:
                fruit.acc.x += fruit.vel.x * fruit.friction
                fruit.vel += fruit.acc
                fruit.pos += fruit.vel + 0.5 * fruit.acc
        else:
            self.moving_on_x_axis()

        self.container_collision(screen)

        if event.type == pygame.MOUSEBUTTONUP and self.mouse_button_pressed:
            self.mouse_button_pressed = False
            self.spawn_new_fruit()

    def spawn_new_fruit(self):
        new_fruit = Fruits((self.pos.x, 100))
        self.fruits_list.append(new_fruit)
        self.follow_mouse = True

    def moving_on_x_axis(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        interpolation_factor = 0.1
        self.pos.x += (mouse_x - self.pos.x) * interpolation_factor

        if self.follow_mouse:
            # Update the position of the last fruit to follow the mouse on the x-axis
            self.fruits_list[-1].pos.x = mouse_x  # Assuming mouse_x is the current mouse x-coordinate
            self.fruits_list[-1].pos.y = 100  # Set y-coordinate as needed

            self.fruits_list[-1].pos.x = max(710, min(self.pos.x, 1272))

    def container_collision(self, screen):
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
        for fruit in self.fruits_list:
            pygame.draw.circle(screen, fruit.color, (int(fruit.pos[0]), int(fruit.pos[1])), fruit.radius)
        pygame.draw.line(screen, "black", self.start_point, self.end_point, self.line_width)