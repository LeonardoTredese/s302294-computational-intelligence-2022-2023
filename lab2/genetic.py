import logging
import random
import numpy as np
import sys
from collections import namedtuple, Counter
from typing import Callable, Generator

logging.basicConfig(format="%(message)s", level=logging.INFO)

def problem(N: int, seed=None) -> list:
    random.seed(seed)
    return list(sorted({ 
        tuple(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    }))

Individual = namedtuple('Individual', ['genome', 'fitness']) 


def gen_fitness(problem: list) -> Callable:
    """ Returns a fitness function based on  the given problem """
    def fitness(genome: np.ndarray) -> tuple:
        """
            Evaluates the fitness of a given genome.
            The fitness is represented as the tuple:
            (# of distinct elements, minus # of elements)
        """
        cnt = Counter()
        for set_, gene in zip(problem, genome):
            if gene:
                cnt.update(set_)
        return len(cnt), -cnt.total()
    return fitness

def init_population(
        population_size: int,
        problem_size: int,
        fitness: Callable,
        rand: np.random.Generator
    ) -> Generator:
    """
        Creates an initial population of a given size for a specific problem.
        The genome components are distributed uniformly, and their fitness is evaluated.
    """
    def new_individual():
        genome = rand.choice([True, False], size=problem_size)
        return Individual(genome, fitness(genome))
    return (new_individual() for _ in range(population_size))

def flip_mutation(genome: np.ndarray, rand: np.random.Generator) -> np.ndarray:
    """ Flips n random  genes of the genome, where n ~ 1 + Pois(1). """
    n_flips = rand.poisson(1) + 1
    flips = rand.integers(len(genome), size = n_flips)
    genome[flips] = ~genome[flips]
    return genome

def loseweight_mutation(genome: np.ndarray, rand: np.random.Generator) -> np.ndarray:
    """ Sets at random some of the True genes to False, therefore reducing weight """
    if np.any(genome):
        pos_index = np.arange(len(genome))[genome]
        drops = rand.choice(pos_index, size=rand.integers(len(pos_index)))
        genome[drops] = False
    return genome

def rand_crossover(genome1: np.ndarray, genome2: np.ndarray, rand: np.random.Generator) -> np.ndarray:
    """ For each locus chooses at random if the gene will come from either genome1 or genome2 """
    mask = rand.choice([True, False], size = len(genome1))
    return np.where(mask, genome1, genome2)

def onecut_crossover(genome1: np.ndarray, genome2: np.ndarray, rand: np.random.Generator) -> np.ndarray:
    """ Vanilla one cut crossover""" 
    split = rand.choice(len(genome1))
    return np.concatenate([genome1[:split], genome2[split:]])

def tournament(population: list, size: int) -> Individual:
    """ Returns the best individual among 'size' random individuals of the given population """
    partecipants = (random.choice(population) for _ in range(size))
    return max(partecipants, key=lambda i: i.fitness)

def create_offspring(population: list, selective_pressure: int, mutation_rate: float, fitness: Callable, rand: np.random.Generator) -> Individual:
        """
            Given a population it selects two parents using tournament selection and a specified selective pressure.
            Then randomly applies a mutation to the new offspring.
        """
        parent1 = tournament(population, selective_pressure)
        parent2 = tournament(population, selective_pressure)
        crossover = rand.choice([rand_crossover, onecut_crossover])
        genome = crossover(parent1.genome, parent2.genome, rand)
        if mutation_rate >= rand.random():
            mutation = rand.choice([flip_mutation, loseweight_mutation])
            genome = mutation(genome, rand)
        return Individual(genome, fitness(genome))

def mutate_population(population: list, mutation_rate: float, fitness: Callable, rand: np.random.Generator) -> Generator:
    """ Mutate the individuals in the population with a chance equalt to the mutation rate """
    def random_mutation(ind: Individual) -> Individual:
        if mutation_rate >= rand.random():
            mutation = rand.choice([flip_mutation, loseweight_mutation])
            genome = mutation(ind.genome, rand)
            ind = Individual(genome, fitness(genome))
        return ind
    return (random_mutation(i) for i in population)

def run_generations(population: list, n_generations: int, offspring_size: int, mutation_rate: float, selective_pressure: int) -> list: 
    """ Pergorm the genetic algorithm with strategy one for n_generations with the given parameters"""
    best_individual = max(population, key=lambda i: i.fitness)
    for generation in range(n_generations):
        population = list(mutate_population(population, mutation_rate, fitness, random_generator))
        offspring = [create_offspring(population, selective_pressure, mutation_rate, fitness, random_generator) for _ in range(offspring_size)]
        population = sorted(population + offspring, key=lambda i: i.fitness, reverse=True)[:offspring_size]
        if population[0].fitness > best_individual.fitness:
            best_individual = population[0]
            logging.debug(f"\rgeneration {generation} weight {-best_individual.fitness[1]}")
    return population, best_individual

for N in [5, 10, 20, 100, 500, 1000]:
    SEED = 42
    P = problem(N, seed = SEED)
    random_generator = np.random.default_rng(SEED)
    fitness = gen_fitness(P)
    population = list(init_population(50, len(P), fitness, random_generator))
    
    population, best_individual = run_generations(population, 1000, 20, .8, 15) 
        
    outcome = f"""For problem of size {N}:
     Found a {"valid" if best_individual.fitness[0] == N else "invalid"} solution
     with weight {-best_individual.fitness[1]:,}"""
    logging.info(outcome) 
