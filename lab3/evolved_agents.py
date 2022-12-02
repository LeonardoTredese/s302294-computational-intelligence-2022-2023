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

def one_lambda(initial, lambda_, fitness, epochs, seed=None) -> tuple:
    one = initial
    best = one
    population, hist = list(), list()
    for epoch in range(epochs):
        tweaked = (one.tweak() for _ in range(lambda_))
        fit, one = max(((fitness(i), i) for i in tweaked), key=lambda x: x[0])        
        hist.append(fit)
        if fit > fitness(best):
            best = one
        population.clear()
    return best, hist

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
    
