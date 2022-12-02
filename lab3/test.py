import random
import numpy.random as nr
import logging
import matplotlib.pyplot as plt
from functools import partial
from game import Nim, Duel
from evolved_agents import nim_fitness, lexicase_nim_fitness, one_lambda, lexicase_evaluator, fitness_hole_evaluator, basic_evaluator
from players import hardcoded_ply, dumb_ply, random_ply, good_ply, human_ply, top_ply, terrible_ply, AdaptivePlayer

logging.basicConfig(format="%(message)s", level=logging.DEBUG)
random.seed(7)
nr.seed(7)
rows = 4
adversaries = [hardcoded_ply, good_ply, random_ply, dumb_ply, terrible_ply]
adv_games = [30, 20, 20, 2, 2]
player = AdaptivePlayer(rows, n_rules=20)

fitness = partial(lexicase_nim_fitness, adversaries=adversaries, rows = rows, n_games = adv_games)
evaluator = partial(lexicase_evaluator, fitness = fitness, fit_dimensions = len(adversaries))

print(fitness(player))
best, history = one_lambda(player, 10, evaluator, 1000)
print(fitness(best))

Duel(Nim(rows), human_ply, best, visible = True).play()

