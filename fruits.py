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
        self.collision_detected = False

        self.start_point = (675, 977)
        self.end_point = (1322, 977)
        self.line_width = 5
        self.fruit_container = FruitContainer()

    def update(self, event, screen):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_button_pressed = True

        for fruit in self.fruits_list:
            fruit.acc.x += fruit.vel.x * fruit.friction
            fruit.vel += fruit.acc
            fruit.pos += fruit.vel + 0.5 * fruit.acc
        
        if self.mouse_button_pressed:
            self.pos.y = 100
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
        for fruit in self.fruits_list:
            fruit_rect = pygame.Rect(fruit.pos.x - fruit.radius, fruit.pos.y - fruit.radius, 2 * fruit.radius, 2 * fruit.radius)

            fruit_container_rect = pygame.Rect(
                self.fruit_container.fruit_container_rect.x,
                self.fruit_container.fruit_container_rect.y,
                self.fruit_container.width,
                self.fruit_container.height
            )

            # Bottom Collision
            if fruit_rect.colliderect(fruit_container_rect) and fruit_rect.bottom >= fruit_container_rect.bottom:
                if fruit.vel.y > 0:
                    fruit.vel.y = -fruit.vel.y / 2
                    fruit.pos.y = min(fruit_rect.bottom, fruit_container_rect.bottom)
                    

            # Right Collision
            if fruit_rect.colliderect(fruit_container_rect) and fruit_rect.right >= fruit_container_rect.right:
                if fruit.vel.x > 0:
                    fruit.vel.x = -fruit.vel.x / 2
                    

            # Left Collision
            if fruit_rect.colliderect(fruit_container_rect) and fruit_rect.left <= fruit_container_rect.left:
                if fruit.vel.x < 0:
                    fruit.vel.x = -fruit.vel.x / 2
                    

            # Other Fruits Collision
            for other_fruit in self.fruits_list:
                if fruit != other_fruit:
                    other_fruit_rect = pygame.Rect(other_fruit.pos.x - other_fruit.radius, other_fruit.pos.y - other_fruit.radius, 2 * other_fruit.radius, 2 * other_fruit.radius)

                    if fruit_rect.colliderect(other_fruit_rect):
                        if not fruit.collision_detected:
                            fruit.collision_detected = True
                            other_fruit.collision_detected = True

                            # Adjust the division factor as needed
                            division_factor = 2

                            # Velocities adjustment
                            fruit.vel.x = -fruit.vel.x / division_factor
                            fruit.vel.y = -fruit.vel.y / division_factor
                            other_fruit.vel.x = -other_fruit.vel.x / division_factor
                            other_fruit.vel.y = -other_fruit.vel.y / division_factor

                            # Check if velocities are too small and set them to zero
                            min_velocity_threshold = 0.1
                            if abs(fruit.vel.x) < min_velocity_threshold:
                                fruit.vel.x = 0
                            if abs(fruit.vel.y) < min_velocity_threshold:
                                fruit.vel.y = 0
                            if abs(other_fruit.vel.x) < min_velocity_threshold:
                                other_fruit.vel.x = 0
                            if abs(other_fruit.vel.y) < min_velocity_threshold:
                                other_fruit.vel.y = 0

                            # Ensure no overlap
                            overlap_x = fruit_rect.right - other_fruit_rect.left if fruit.vel.x > 0 else other_fruit_rect.right - fruit_rect.left
                            overlap_y = fruit_rect.bottom - other_fruit_rect.top if fruit.vel.y > 0 else other_fruit_rect.bottom - fruit_rect.top
                            fruit.pos.x += overlap_x / 2
                            fruit.pos.y += overlap_y / 2
                            other_fruit.pos.x -= overlap_x / 2
                            other_fruit.pos.y -= overlap_y / 2

                        else:
                            fruit.collision_detected = False
                            other_fruit.collision_detected = False
                
    def draw(self, screen):
        for fruit in self.fruits_list:
            pygame.draw.circle(screen, fruit.color, (int(fruit.pos[0]), int(fruit.pos[1])), fruit.radius)