import logging
import random
import numpy as np
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
    return [ new_individual() for _ in range(population_size) ]

def flip_mutation(genome: np.ndarray, rand: np.random.Generator) -> np.ndarray:
    n_flips = rand.poisson(1) + 1
    flips = rand.integers(len(genome), size = n_flips)
    genome[flips] = ~genome[flips]
    return genome

def no_mutation(genome: np.ndarray, mock) -> np.ndarray:
    return genome

def rand_crossover(genome1: np.ndarray, genome2: np.ndarray, rand: np.random.Generator) -> np.ndarray:
    new_genome = np.full(len(genome1), False)
    mask = rand.choice([True, False], size = len(new_genome))
    new_genome[mask] = genome1[mask]
    new_genome[~mask] = genome2[~mask]
    return new_genome

def tournament(population: list, size: int, rand: np.random.Generator) -> Individual:
    # choice returns a 2d array of objects instead of 1d array of individuals
    partecipants = rand.choice(population, size = size)
    return Individual(*max(partecipants, key=lambda i: i[1]))

def create_offspring(population: list, selective_pressure: int, rand: np.random.Generator) -> Individual:
        parent1 = tournament(population, 15, rand)
        parent2 = tournament(population, 15, rand)
        genome = rand_crossover(parent1.genome, parent2.genome, rand)
        mutation = rand.choice([no_mutation, flip_mutation])
        genome = mutation(genome, rand)
        return Individual(genome, fitness(genome))

N = 500
SEED = 42
P = problem(N, seed = SEED)
OFFSPRING_SIZE = 20
random_generator = np.random.default_rng(SEED)
fitness = gen_fitness(P)
population = init_population(100, len(P), fitness, random_generator)
best_individual = max(population, key=lambda i: i.fitness)


for _ in range(10_000):
    offspring = [create_offspring(population, 15, random_generator) for _ in range(OFFSPRING_SIZE)]
    best_offspring = max(offspring, key=lambda i: i.fitness)
    if best_offspring.fitness > best_individual.fitness:
        best_individual = best_offspring
        print('\r', _, best_individual, end='')
    population = sorted(population, key=lambda i: i.fitness)
    population[:OFFSPRING_SIZE] = offspring
 
