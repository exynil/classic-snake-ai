import pickle

import pygame
import field
import random
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from settings import settings
import numpy
import os


def random_weights():
    return random.uniform(-0.1, 0.1)


class GeneticAlgorithm:
    def __init__(self):
        random.seed(settings['random_seed'])
        pygame.init()
        self.field = field.Field(self, settings['field_width'], settings['field_height'])
        self.checkpoint = f"checkpoints/checkpoint_{settings['checkpoint']}.pkl"
        self.gen_counter = 0
        self.ind_counter = 0
        self.pop_length = 0

    def start(self):
        if not os.path.exists('checkpoints'):
            os.makedirs('checkpoints')

        toolbox = base.Toolbox()
        creator.create('FitnessMax', base.Fitness, weights=(1.0,))
        creator.create('Individual', list, fitness=creator.FitnessMax)
        toolbox.register('individual_creator', tools.initRepeat, creator.Individual, random_weights,
                         settings['weights_length'])
        toolbox.register('population_creator', tools.initRepeat, list, toolbox.individual_creator)
        toolbox.register('evaluate', self.field.get_fitness)
        toolbox.register('select', tools.selTournament, tournsize=3)
        toolbox.register('mate', tools.cxTwoPoint)
        toolbox.register('mutate', tools.mutPolynomialBounded, low=-1.0, up=0.3, eta=35, indpb=0.5)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register('max', numpy.max)
        stats.register('avg', numpy.mean)

        if os.path.exists(self.checkpoint):
            with open(self.checkpoint, 'rb') as cp_file:
                cp = pickle.load(cp_file)
                population = cp['population']
                start_gen = cp['generation']
                hall_of_fame = cp['hall_of_fame']
                logbook = cp['logbook']
                random.setstate(cp['random_state'])
                self.field.set_death_stats(cp['death_stats'])
                self.field.snake.set_high_score(cp['high_score'])
        else:
            population = toolbox.population_creator(n=settings['population_size'])

            logbook = tools.Logbook()
            logbook.header = 'gen', 'ind', 'max', 'avg'

            hall_of_fame = tools.HallOfFame(settings['hall_of_fame_size'])

            start_gen = 2

            invalid_ind = [ind for ind in population if not ind.fitness.valid]

            self.pop_length = len(invalid_ind)
            self.gen_counter = 1

            fitness_values = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitness_values):
                ind.fitness.values = fit

            record = stats.compile(population) if stats else {}
            logbook.record(gen=1, ind=len(invalid_ind), **record)

            print(logbook.stream)

        hall_of_fame.update(population)
        hof_size = len(hall_of_fame.items) if hall_of_fame.items else 0

        for gen in range(start_gen, settings['max_generations'] + 1):

            offspring = toolbox.select(population, len(population) - hof_size)

            offspring = algorithms.varAnd(offspring, toolbox, settings['p_crossover'], settings['p_mutation'])

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

            self.gen_counter = gen
            self.ind_counter = 0
            self.pop_length = len(invalid_ind)

            fitness_values = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitness_values):
                ind.fitness.values = fit

            offspring.extend(hall_of_fame.items)

            hall_of_fame.update(offspring)

            population[:] = offspring

            record = stats.compile(population) if stats else {}
            logbook.record(gen=gen, ind=len(invalid_ind), **record)

            cp = dict(population=population, generation=gen + 1, hall_of_fame=hall_of_fame,
                      logbook=logbook, random_state=random.getstate(), death_stats=self.field.get_death_stats(),
                      high_score=self.field.snake.get_high_score())

            with open(f'checkpoints/checkpoint_{gen}.pkl', 'wb') as cp_file:
                pickle.dump(cp, cp_file)

            print(logbook.stream)
