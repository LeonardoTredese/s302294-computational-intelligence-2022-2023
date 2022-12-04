import random
import numpy as np
from typing import Callable, Iterable
from functools import reduce
from itertools import chain
from game import Duel, Nim

class SelfAdaptiveParameters:
    """ tweakable parameters using self-adaptation algorithm """
    def __init__(self, initial_params: np.ndarray, sigma: np.ndarray, seed: int = None, step: int = 1) -> None:
        self._generator = np.random.default_rng(0 if seed is None else seed)
        self._v = initial_params
        self._shape = initial_params.shape
        self._sigma = sigma
        self._step = step        

    def tweak(self):
        tau = 1 / (self._step ** .5)
        seed = self._generator.integers(2 ** 10)
        sigma = self._sigma * np.exp(tau * self._generator.normal(size = self._shape))
        value = self._generator.normal(loc=self._v, scale=self._sigma)
        return SelfAdaptiveParameters(value, sigma, seed=seed, step=self._step+1)
   
    def __getitem__(self, key: int | slice) -> float:
        return self._v[key]

def one_lambda(initial: object, lambda_: int, evaluator: Callable, epochs: int) -> tuple:
    """ (1, lambda) Evolutionary Search """
    one = initial
    hist = list()
    for epoch in range(epochs):
        tweaked = (one.tweak() for _ in range(lambda_))
        fit, one = evaluator(tweaked) 
        hist.append((fit, one))
    return one, hist
        
def nim_fitness(individual: Callable, adversary: Callable, rows: int = 3,  n_games: int = 100) -> float:
    wins = 0
    for game_id in range(n_games):
        game = Nim(rows)
        if game_id % 2:
            duel = Duel(game, adversary, individual)
            wins += duel.play()
        else:
            duel = Duel(game, individual, adversary)
            wins += 1 - duel.play()
    return wins / n_games

def lexicase_nim_fitness(individual: Callable, adversaries: Iterable[Callable] = list(), rows: int = 3, n_games: Iterable[int] = list()):
    return tuple((nim_fitness(individual, adversary, rows=rows, n_games=games) for adversary, games in zip(adversaries, n_games)))
    
def lexicase_evaluator(population: Iterable, fitness: Callable = lexicase_nim_fitness, fit_dimensions: int = 1) -> tuple:
    """ Given a population extract best individual using lexicase selection """
    evaluated = ((fitness(i), i) for i in population)
    shuffle = random.sample(range(fit_dimensions), fit_dimensions)
    fitness_shuffle = lambda f: tuple(f[i] for i in shuffle)
    return max(evaluated, key = lambda e: fitness_shuffle(e[0]))

def scalar_evaluator(population: Iterable, fitness: Callable = nim_fitness) -> tuple:
    """ Given a population extract most fit individual """
    return max(((fitness(i), i) for i in population), key = lambda e: e[0])

