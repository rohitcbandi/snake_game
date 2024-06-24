import pygame
import random
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Screen size
width, height = 400, 400
cell_size = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.snake = [(width//2, height//2)]
        self.generate_food()
        self.done = False
        self.score = 0
        return self.get_state()

    def generate_food(self):
        self.food = (random.randint(0, (width-cell_size)//cell_size) * cell_size,
                     random.randint(0, (height-cell_size)//cell_size) * cell_size)
        while self.food in self.snake:
            self.food = (random.randint(0, (width-cell_size)//cell_size) * cell_size,
                         random.randint(0, (height-cell_size)//cell_size) * cell_size)

    def step(self, action):
        if action == 0:  # Straight
            pass
        elif action == 1:  # Right turn
            if self.direction == 'UP':
                self.direction = 'RIGHT'
            elif self.direction == 'RIGHT':
                self.direction = 'DOWN'
            elif self.direction == 'DOWN':
                self.direction = 'LEFT'
            elif self.direction == 'LEFT':
                self.direction = 'UP'
        elif action == 2:  # Left turn
            if self.direction == 'UP':
                self.direction = 'LEFT'
            elif self.direction == 'LEFT':
                self.direction = 'DOWN'
            elif self.direction == 'DOWN':
                self.direction = 'RIGHT'
            elif self.direction == 'RIGHT':
                self.direction = 'UP'

        head_x, head_y = self.snake[0]
        if self.direction == 'UP':
            head_y -= cell_size
        elif self.direction == 'DOWN':
            head_y += cell_size
        elif self.direction == 'LEFT':
            head_x -= cell_size
        elif self.direction == 'RIGHT':
            head_x += cell_size

        self.snake.insert(0, (head_x, head_y))

        if self.snake[0] == self.food:
            self.score += 1
            self.generate_food()
        else:
            self.snake.pop()

        if (head_x < 0 or head_x >= width or head_y < 0 or head_y >= height or
                len(self.snake) != len(set(self.snake))):
            self.done = True

        return self.get_state(), self.reward(), self.done

    def get_state(self):
        head_x, head_y = self.snake[0]
        state = [
            head_x == self.food[0] and head_y > self.food[1],  # Food up
            head_x == self.food[0] and head_y < self.food[1],  # Food down
            head_y == self.food[1] and head_x > self.food[0],  # Food left
            head_y == self.food[1] and head_x < self.food[0],  # Food right
            self.direction == 'UP', self.direction == 'DOWN',
            self.direction == 'LEFT', self.direction == 'RIGHT',
            head_y == 0 or (head_x, head_y-cell_size) in self.snake,  # Up danger
            head_y == height-cell_size or (head_x, head_y+cell_size) in self.snake,  # Down danger
            head_x == 0 or (head_x-cell_size, head_y) in self.snake,  # Left danger
            head_x == width-cell_size or (head_x+cell_size, head_y) in self.snake  # Right danger
        ]
        return np.array(state, dtype=int)

    def reward(self):
        if self.done:
            return -10
        if self.snake[0] == self.food:
            return 10
        return 0

    def render(self):
        self.screen.fill(BLACK)
        for x, y in self.snake:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(x, y, cell_size, cell_size))
        pygame.draw.rect(self.screen, RED, pygame.Rect(self.food[0], self.food[1], cell_size, cell_size))
        pygame.display.flip()
        self.clock.tick(10)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
