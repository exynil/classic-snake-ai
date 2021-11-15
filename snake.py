import numpy as np
from settings import settings
import pygame
from pygame import Vector2

from neural_network import NeuralNetwork


class Snake:
    def __init__(self, sc, field):
        self.sc = sc
        self.field = field
        self.path = []
        self.nn = NeuralNetwork(24, 18, 12, 4)
        self.color = pygame.Color('#50FA7B')
        self.path_color = pygame.Color('#BD93F9')
        self.vector_color = pygame.Color('#BD93F9')
        self.size = 40
        self.high_score = 0
        self.length = None
        self.steps = None
        self.score = None
        self.energy = None
        self.directions = [
            Vector2(0, -40),     # up
            Vector2(40, 0),      # right
            Vector2(0, 40),      # down
            Vector2(-40, 0)      # left
        ]
        self.vectors = [
           Vector2(0, -40),     # up
           Vector2(40, -40),    # up and right
           Vector2(40, 0),      # right
           Vector2(40, 40),     # down and right
           Vector2(0, 40),      # down
           Vector2(-40, 40),    # down and left
           Vector2(-40, 0),     # left
           Vector2(-40, -40)    # up and left
        ]

    def reset(self):
        self.score = 0
        self.steps = 0
        self.length = 3
        self.energy = settings['snake_energy']
        self.path.clear()
        self.path.append(self.field.get_random_pos())
        if settings['smart_speed']:
            settings['slow_mode'] = False

    def draw(self):
        [(pygame.draw.rect(self.sc, self.color, (i, j, self.size, self.size))) for i, j in self.path[-self.length:]]

    def draw_footprint(self):
        if len(self.path) > 6:
            points = [[a + self.size / 2, b + self.size / 2] for a, b in self.path[:-self.length]]
            pygame.draw.aalines(self.sc, self.path_color, False, points)

    def draw_vectors(self):
        for v in self.vectors:
            counter = 0
            pos = self.get_head()
            while self.field.is_valid_pos(pos + v):
                pos += v
                counter += 1
                font = pygame.font.Font('./fonts/TerminusTTF.ttf', 12)
                render = font.render(f'{counter}', True, self.vector_color)
                self.sc.blit(render, pos + Vector2(12, 12))

    def move(self):
        inputs = self.dist_to_wall() + self.dist_to_self() + self.dist_to_food()

        index = np.argmax(self.nn.query([1 / x if x > 0 else 0.025 for x in inputs]))

        new_pos = self.get_head() + self.directions[index]

        self.path.append(new_pos)

        if len(self.path) > self.length + 20:
            self.path.pop(0)

        self.steps += 1
        self.energy -= 1

    def dist_to_wall(self):
        inputs = []

        for v in self.vectors:
            counter = 0
            pos = self.get_head()
            while self.field.is_valid_pos(pos):
                pos += v
                counter += 1
            inputs.append(counter)

        return inputs

    def dist_to_self(self):
        inputs = [0] * 8

        for v in self.vectors:
            counter = 0
            pos = self.get_head()
            while self.field.is_valid_pos(pos):
                pos += v
                counter += 1

                if pos in self.path[-self.length:-1]:
                    inputs[self.vectors.index(v)] = counter
                    break

        return inputs

    def dist_to_food(self):
        inputs = [0] * 8
        apple_pos = self.field.get_apple_pos()

        for v in self.vectors:
            counter = 0
            pos = self.get_head()
            while self.field.is_valid_pos(pos):
                pos += v
                counter += 1
                if pos == apple_pos:
                    inputs[self.vectors.index(v)] = counter
                    return inputs

        return inputs

    def get_head(self):
        return Vector2(self.path[-1])

    def get_segments(self):
        return self.path[-self.length:]

    def check_apple_collision(self):
        if self.get_head() == self.field.get_apple_pos():
            self.score += 1
            self.length += 1
            self.energy += settings['snake_energy']
            if self.score > self.high_score:
                self.high_score = self.score

            if settings['smart_speed'] and self.score > 5:
                settings['slow_mode'] = True
            return True
        return False

    def check_wall_collision(self):
        if not self.field.is_valid_pos(self.get_head()):
            return True
        return False

    def check_self_collision(self):
        if self.get_head() in self.path[-self.length:-1]:
            return True
        return False

    def check_energy(self):
        return self.energy < 0

    def get_fitness(self):
        return self.steps**2 * 2**self.score,

    def get_energy(self):
        return self.energy

    def load_weights(self, individual):
        self.nn.load_weights(individual)

    def get_high_score(self):
        return self.high_score

    def set_high_score(self, score):
        self.high_score = score
