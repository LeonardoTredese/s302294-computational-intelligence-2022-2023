import random
import logging
from functools import partial
from game import Nim, Duel
from evolved_agents import nim_fitness, one_lambda
from players import dumb_ply, random_ply, good_ply, human_ply, top_ply, terrible_ply, AdaptivePlayer

logging.basicConfig(format="%(message)s", level=logging.INFO)
random.seed(42)
rows = 10
player = AdaptivePlayer(rows)
fitness = partial(nim_fitness, adversary = dumb_ply, rows = rows, n_games = 2)

print(fitness(player))
best, history = one_lambda(player, 10, fitness, 100)
print(history)

print(nim_fitness(best, adversary = terrible_ply, rows = rows, n_games = 100))
print(nim_fitness(best, adversary = dumb_ply, rows = rows, n_games = 100))
print(nim_fitness(best, adversary = random_ply, rows = rows, n_games = 100))
print(nim_fitness(best, adversary = good_ply, rows = rows, n_games = 100))
# print(nim_fitness(best, adversary = top_ply, rows = rows, n_games = 100))
# Duel(Nim(rows), human_ply, best).play()

