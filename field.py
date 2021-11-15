import pygame
from random import randrange
from settings import settings
from pygame import Vector2
from snake import Snake
from apple import Apple


def pause():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                settings['snake_footprint'] = not settings['snake_footprint']
            if event.key == pygame.K_v:
                settings['snake_vectors'] = not settings['snake_vectors']
            if event.key == pygame.K_g:
                settings['grid'] = not settings['grid']
            if event.key == pygame.K_s:
                settings['slow_mode'] = not settings['slow_mode']
            if event.key == pygame.K_i:
                settings['info'] = not settings['info']
            if event.key == pygame.K_m:
                settings['smart_speed'] = not settings['smart_speed']
            if event.key == pygame.K_a:
                settings['animation'] = not settings['animation']
            if event.key == pygame.K_q:
                exit(0)
            if event.key == pygame.K_SPACE:
                pause()


class Field:
    def __init__(self, ga, width, height):
        self.ga = ga
        self.width = width
        self.height = height
        self.sc = pygame.display.set_mode([width + 1, height + 1])
        self.clock = pygame.time.Clock()
        self.snake = Snake(self.sc, self)
        self.apple = Apple(self.sc, self)
        self.death_stats = [0] * 3
        pygame.init()

    def get_fitness(self, individual):
        self.ga.ind_counter += 1
        self.snake.reset()
        self.snake.load_weights(individual)
        self.apple.reset()

        while True:
            self.snake.move()
            self.draw()

            if self.snake.check_apple_collision():
                self.apple.reset()

            if self.snake.check_wall_collision():
                self.death_stats[0] += 1
                break

            if self.snake.check_self_collision():
                self.death_stats[1] += 1
                break

            if self.snake.check_energy():
                self.death_stats[2] += 1
                break

            check_events()

        return self.snake.get_fitness()

    # Проверяем не вышла ли голова змейки на границы поля
    def is_valid_pos(self, pos):
        if pos.x < 0 or pos.x > self.width - self.snake.size or pos.y < 0 or pos.y > self.height - self.snake.size:
            return False
        return True

    # Получаем случайную позицию на поле [доработать]
    def get_random_pos(self):
        while True:
            pos = Vector2(randrange(0, self.width, self.snake.size), randrange(0, self.height, self.snake.size))
            if pos not in self.snake.get_segments():
                return pos

    def get_apple_pos(self):
        return self.apple.get_pos()

    def set_death_stats(self, death_stats):
        self.death_stats = death_stats

    def get_death_stats(self):
        return self.death_stats

    def draw(self):
        if settings['animation']:
            self.sc.fill(pygame.Color('#282A36'))
            if settings['grid']:
                self.draw_grid()
            if settings['info']:
                self.draw_info()
            if settings['snake_footprint']:
                self.snake.draw_footprint()
            if settings['snake_vectors']:
                self.snake.draw_vectors()

            self.snake.draw()
            self.apple.draw()
            pygame.display.flip()

            if settings['slow_mode']:
                self.clock.tick(settings['fps'])

    def draw_grid(self):
        for x in range(0, self.width + self.snake.size, self.snake.size):
            pygame.draw.aaline(self.sc, '#44475a', [x, 0], [x, self.height])
        for y in range(0, self.height + self.snake.size, self.snake.size):
            pygame.draw.aaline(self.sc, '#44475a', [0, y], [self.width, y])

    def draw_info(self):
        self.draw_text(20, 20, f'HIGH SCORE: {self.snake.high_score}')
        self.draw_text(20, 40, f'GENERATION: {self.ga.gen_counter}')
        self.draw_text(20, 60, f'GENOME: {self.ga.ind_counter}/{self.ga.pop_length}')
        self.draw_text(20, 80, f'SCORE: {self.snake.score}')
        self.draw_text(20, 100, f'STEPS: {self.snake.steps}')
        self.draw_text(20, 120, f'ENERGY: {self.snake.get_energy()}')
        if sum(self.death_stats) != 0:
            percent = '{:.2f}'.format(self.death_stats[0] * 100 / sum(self.death_stats))
            self.draw_text(20, 140, f'BUMPED INTO A WALL: {self.death_stats[0]} | {percent}%')
            percent = '{:.2f}'.format(self.death_stats[1] * 100 / sum(self.death_stats))
            self.draw_text(20, 160, f'HIT ITS OWN TAIL: {self.death_stats[1]} | {percent}%')
            percent = '{:.2f}'.format(self.death_stats[2] * 100 / sum(self.death_stats))
            self.draw_text(20, 180, f'DIED OF HUNGER: {self.death_stats[2]} | {percent}%')

        self.draw_text(20, 220, f'HOTKEYS:')
        self.draw_text(20, 240, f'A - evolution without animation')
        self.draw_text(20, 260, f'S - slow/fast')
        self.draw_text(20, 280, f'M - smart speed')
        self.draw_text(20, 300, f'F - footprint')
        self.draw_text(20, 320, f'V - vectors')
        self.draw_text(20, 340, f'G - grid')
        self.draw_text(20, 360, f'I - info')

        self.draw_text(20, 400, f'Snake: [ {self.snake.get_head().x}, {self.snake.get_head().y} ]')
        self.draw_text(20, 420, f'Apple: [ {self.apple.get_pos().x}, {self.apple.get_pos().x} ]')

    def draw_text(self, x, y, text):
        font = pygame.font.Font('./fonts/TerminusTTF.ttf', 14)
        self.sc.blit(font.render(text, True, pygame.Color('#50FA7B')), (x, y))
