import pygame
import math
import random
from fruits import Fruit

class FruitGame:
    def __init__(self):
        pygame.init()
        self.screen_width = 600
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.skewed_probability = [0.7, 0.1, 0.05, 0.08, 0.04, 0.02, 0.01, 0, 0]
        self.colors = [(255, 255, 255), (255, 0, 0), (255, 165, 0), (255, 255, 0),
                       (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 105, 180), (128, 0, 128)]
        self.color_order = self.colors.copy()
        self.radius_order = [15, 22, 42, 55, 68, 85, 94, 110, 130]
        self.gravity = 0.05

        self.fruits = []
        self.fruits_to_add = []
        self.fruits_to_remove = []

        self.score = 0
        self.score_order = [0, 2, 4, 8, 8, 16, 32, 64, 128]

        self.fruit_speed = 1

        self.running = True
        self.game_over = False

        self.init_game()

    def init_game(self):
        self.create_screen()
        self.setup_game()

    def create_screen(self):
        pygame.display.set_caption("Fruit Game")

    def setup_game(self):
        self.next_fruit_index = random.choices(range(len(self.color_order)),
                                              weights=self.skewed_probability, k=1)[0]
        self.next_fruit_radius = self.radius_order[self.next_fruit_index]
        self.next_fruit_color = self.color_order[self.next_fruit_index]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)

    def handle_mouse_click(self, event):
        if 40 < event.pos[0] < 560 and event.pos[1] < 40:
            fruit_x = event.pos[0]
            fruit_y = event.pos[1]
            horizontal_speed = 0
            is_dropping = True
            self.fruits.append(Fruit(fruit_x, fruit_y, self.fruit_speed,
                                   horizontal_speed, self.next_fruit_color,
                                   self.next_fruit_radius, is_dropping))
            self.update_next_fruit()

    def handle_mouse_motion(self, event):
        mouse_x = event.pos[0]
        mouse_y = 25
        pygame.draw.circle(self.screen, self.next_fruit_color, (mouse_x, mouse_y), self.next_fruit_radius)

    def update_next_fruit(self):
        self.next_fruit_index = random.choices(range(len(self.color_order)),
                                              weights=self.skewed_probability, k=1)[0]
        self.next_fruit_color = self.color_order[self.next_fruit_index]
        self.next_fruit_radius = self.radius_order[self.next_fruit_index]

    def check_collision(self):
        #online
        for i in range(len(self.fruits)):
            for j in range(i + 1, len(self.fruits)):
                dx = self.fruits[i].x - self.fruits[j].x
                dy = self.fruits[i].y - self.fruits[j].y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance < self.fruits[i].radius + self.fruits[j].radius:
                    if self.fruits[i].color == self.fruits[j].color:
                        color_index = self.color_order.index(self.fruits[i].color)
                        if color_index == len(self.color_order) - 1:
                            self.score += self.score_order[color_index] * 2
                        if color_index + 1 < len(self.color_order):
                            new_x = (self.fruits[i].x + self.fruits[j].x) / 2 + random.uniform(-1, 1)
                            new_y = (self.fruits[i].y + self.fruits[j].y) / 2 + random.uniform(0, 1)
                            self.fruits_to_add.append(Fruit(new_x, new_y, self.fruits[i].speed,
                                                           self.fruits[i].horizontal_speed + self.fruits[j].horizontal_speed,
                                                           self.color_order[color_index + 1],
                                                           self.radius_order[color_index + 1], False))
                            self.score += self.score_order[color_index + 1]
                        self.fruits_to_remove.append(self.fruits[i])
                        self.fruits_to_remove.append(self.fruits[j])
                        break
                    else:
                        overlap = self.fruits[i].radius + self.fruits[j].radius - distance
                        dx = dx / distance
                        dy = dy / distance
                        self.fruits[i].x += dx * overlap / 2
                        self.fruits[i].y += dy * overlap / 2
                        self.fruits[j].x -= dx * overlap / 2
                        self.fruits[j].y -= dy * overlap / 2
                        self.fruits[i].speed = 0
                        self.fruits[j].speed = 0
                        self.fruits[i].horizontal_speed *= 1
                        self.fruits[j].horizontal_speed *= 1
                        self.fruits[i].is_dropping = False
                        self.fruits[j].is_dropping = False

        for fruit in self.fruits_to_remove:
            if fruit in self.fruits:
                self.fruits.remove(fruit)
        for fruit in self.fruits_to_add:
            self.fruits.append(fruit)
        self.fruits_to_remove.clear()
        self.fruits_to_add.clear()

    def update_fruits(self):
        for fruit in self.fruits:
            box_top = 40
            if (not fruit.is_dropping) and fruit.y - fruit.radius < box_top:
                self.game_over = True
                break
            fruit.speed += self.gravity
            box_bottom = 720 - fruit.radius
            box_left = 40 + fruit.radius
            box_right = 560 - fruit.radius
            if fruit.y >= box_bottom:
                fruit.y = box_bottom
            elif fruit.y < box_bottom:
                fruit.y += fruit.speed

            fruit.x += fruit.horizontal_speed
            if fruit.x < box_left:
                fruit.x = box_left + 1
                fruit.horizontal_speed *= -0.5
            elif fruit.x > box_right:
                fruit.x = box_right - 1
                fruit.horizontal_speed *= -0.5
            pygame.draw.circle(self.screen, fruit.color, (int(fruit.x), int(fruit.y)), fruit.radius)

    def run_game(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.handle_events()

            if not self.game_over:
                self.check_collision()
                self.update_fruits()

                # Draw 3 lines to make a rectangle with the upper side open
                pygame.draw.line(self.screen, (255, 255, 255), (40, 40), (40, 720), 1)
                pygame.draw.line(self.screen, (255, 255, 255), (40, 720), (560, 720), 1)
                pygame.draw.line(self.screen, (255, 255, 255), (560, 720), (560, 40), 1)

                # Draw a warning line at the top of the box with a red dotted line
                dotted_line_y = 40
                dotted_line_length = 4
                dotted_line_space = 4
                dotted_line_color = (128, 128, 128)
                for x in range(40, 560, dotted_line_length + dotted_line_space):
                    pygame.draw.line(self.screen, dotted_line_color, (x, dotted_line_y),
                                     (x + dotted_line_length, dotted_line_y), 1)

                # Draw color order
                color_order_y = self.screen_height - 20
                color_order_spacing = 40
                for i, color in enumerate(self.color_order):
                    pygame.draw.circle(self.screen, color, (40 + i * color_order_spacing, color_order_y), 10)

                # Draw score
                font = pygame.font.Font(None, 36)
                score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
                self.screen.blit(score_text, (self.screen_width / 2 - score_text.get_width() / 2, 20))

                pygame.display.update()
                self.clock.tick(60)
            elif self.game_over:
                self.handle_game_over()

    def handle_game_over(self):
        font = pygame.font.Font(None, 36)
        game_over_text_lines = [
            "GAME OVER",
            f"Your Score is: {self.score}",
            "Restart by pressing SPACE",
            "Quit game by pressing ESCAPE"
        ]
        for i, line in enumerate(game_over_text_lines):
            line_text = font.render(line, True, (255, 255, 255))
            self.screen.blit(line_text, (self.screen_width / 2 - line_text.get_width() / 2,
                                         self.screen_height / 2 - line_text.get_height() / 2 + i * line_text.get_height()))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset game when space is pressed
                    self.fruits.clear()
                    self.fruits_to_add.clear()
                    self.fruits_to_remove.clear()
                    self.score = 0
                    self.game_over = False
                    self.setup_game()
                elif event.key == pygame.K_ESCAPE:
                    # Quit game when ESC is pressed
                    self.running = False


if __name__ == "__main__":
    game_app = FruitGame()
    game_app.run_game()
    pygame.quit()