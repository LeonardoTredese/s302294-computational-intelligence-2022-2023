import random
import numpy as np
from typing import Callable
from itertools import chain
from game import Duel, Nim

class SelfAdaptiveParameters:
    def __init__(self, initial_params: np.ndarray, sigma: np.ndarray, seed: int = None, step: int = 1) -> None:
        self._generator = np.random.default_rng(seed)
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
   
    def __getitem__(self, key: int) -> float:
        return self._v[key]

def one_lambda(initial: object, lambda_: int, evaluator: Callable, epochs: int) -> tuple:
    one = initial
    best = one
    fit_best = None
    hist = list()
    for epoch in range(epochs):
        tweaked = (one.tweak() for _ in range(lambda_))
        fit, one = evaluator(tweaked) 
        hist.append(fit)
        if fit_best is None or fit > fit_best:
            best = one
            fit_best = fit
    return best, hist

def lexicase_nim_fitness(individual: Callable, adversaries: list[Callable] = list(), rows: int = 3, n_games: list[int] = list()):
    return tuple((nim_fitness(individual, adversary, rows=rows, n_games=games) for adversary, games in zip(adversaries, n_games)))
        
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
    
def lexicase_evaluator(population, fitness: Callable = lexicase_nim_fitness, fit_dimensions: int = 1) -> tuple:
    evaluated = ((fitness(i), i) for i in population)
    random_order = random.sample(range(fit_dimensions), fit_dimensions)
    fitness_sort = lambda f: tuple((f[i] for i in random_order))
    return max(evaluated, key = lambda e: fitness_sort(e[0]))

def fitness_hole_evaluator(population, fitness: Callable = lexicase_nim_fitness, fit_dimensions: int = 1) -> tuple:
    evaluated = ((fitness(i), i) for i in population)
    i = random.randrange(fit_dimensions)
    return max(evaluated, key = lambda e: e[0][i])

def basic_evaluator(population, fitness: Callable = nim_fitness) -> tuple:
    return max(((fitness(i), i) for i in population), key = lambda e: e[0])

