from pygame import Vector2
import pygame


class Apple:
    def __init__(self, sc, field):
        self.sc = sc
        self.field = field
        self.pos = None
        self.color = pygame.Color('#BD93F9')
        self.size = 40

    def reset(self):
        self.pos = self.field.get_random_pos()

    def get_pos(self):
        return Vector2(self.pos)

    def draw(self):
        pygame.draw.rect(self.sc, self.color, [self.pos, Vector2(self.size, self.size)])
