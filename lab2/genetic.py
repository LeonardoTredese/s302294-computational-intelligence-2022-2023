import logging
import random
import numpy as np
import sys
from collections import namedtuple
from typing import Callable

def problem(N: int, seed=None) -> list:
    random.seed(seed)
    return list(sorted({ 
        tuple(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    }))

Individual = namedtuple('Individual', ['genome', 'fitness']) 


def gen_fitness(problem: list) -> Callable:
    def fitness(genome: np.ndarray) -> tuple:
        distinct_numbers = set()
        weight = 0
        for set_, gene in zip(problem, genome):
            if gene:
                distinct_numbers.update(set_)
                weight += len(set_)
        return len(distinct_numbers), -weight
    return fitness

def init_population(
        population_size: int,
        problem_size: int,
        fitness: Callable,
        rand: np.random.Generator
    ) -> list:
    def new_individual():
        genome = rand.choice([True, False], size=problem_size)
        return Individual(genome, fitness(genome))
    return (new_individual() for _ in range(population_size))

def flip_mutation(genome: np.ndarray, rand: np.random.Generator) -> np.ndarray:
    n_flips = rand.poisson(1) + 1
    flips = rand.integers(len(genome), size = n_flips)
    genome[flips] = ~genome[flips]
    return genome

def loseweight_mutation(genome: np.ndarray, rand: np.random.Generator) -> np.ndarray:
    if np.any(genome):
        pos_index = np.arange(len(genome))[genome]
        drops = rand.choice(pos_index, size=rand.integers(len(pos_index)))
        genome[drops] = False
    return genome

def rand_crossover(genome1: np.ndarray, genome2: np.ndarray, rand: np.random.Generator) -> np.ndarray:
    mask = rand.choice([True, False], size = len(genome1))
    return np.where(mask, genome1, genome2)

def onecut_crossover(genome1: np.ndarray, genome2: np.ndarray, rand: np.random.Generator) -> np.ndarray:
    split = rand.choice(len(genome1))
    return np.concatenate([genome1[:split], genome2[split:]])

def tournament(population: list, size: int) -> Individual:
    partecipants = (random.choice(population) for _ in range(size))
    return max(partecipants, key=lambda i: i.fitness)

def create_offspring(population: list, selective_pressure: int, mutation_rate: float, rand: np.random.Generator) -> Individual:
        parent1 = tournament(population, selective_pressure)
        parent2 = tournament(population, selective_pressure)
        crossover = rand.choice([rand_crossover, onecut_crossover])
        genome = crossover(parent1.genome, parent2.genome, rand)
        if mutation_rate >= rand.random():
            mutation = rand.choice([flip_mutation, loseweight_mutation])
            genome = mutation(genome, rand)
        return Individual(genome, fitness(genome))

N = 500
SEED = 42
P = problem(N, seed = SEED)
OFFSPRING_SIZE = 20
random_generator = np.random.default_rng(SEED)
fitness = gen_fitness(P)
population = list(init_population(100, len(P), fitness, random_generator))
best_individual = max(population, key=lambda i: i.fitness)


for _ in range(10_000):
    offspring = [create_offspring(population, 15, .7, random_generator) for _ in range(OFFSPRING_SIZE)]
    population = sorted(population + offspring, key=lambda i: i.fitness, reverse=True)[:OFFSPRING_SIZE]
    if population[0].fitness > best_individual.fitness:
        best_individual = population[0]
        print('\repoch', _,'fitness', -best_individual.fitness[1], end='')
    
 
