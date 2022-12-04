import random
import numpy.random as nr
import logging
import matplotlib.pyplot as plt
from functools import partial
from game import Nim, Duel
from evolved_agents import nim_fitness, lexicase_nim_fitness, one_lambda, lexicase_evaluator, scalar_evaluator
from players import hardcoded_ply, random_ply, good_ply, human_ply, top_ply, AdaptivePly, HybridPly

logging.basicConfig(format="%(message)s", level=logging.INFO)
random.seed(7)
nr.seed(7)
rows = 5
simulations = 100

def log_fitness(plies: list, fitness: callable) -> None:
    for ply in plies:
        logging.info(f" - {ply.__name__}: {fitness(ply)}")
    logging.info("")

logging.info("Test plies against random:")
fitness = partial(nim_fitness, adversary = random_ply, rows = rows, n_games = simulations)
log_fitness([good_ply, hardcoded_ply, top_ply], fitness)

logging.info("Test evolvable plies against random:")

logging.info("before evolution")
adaptive_ply = AdaptivePly(rows)
hybrid_ply = HybridPly(rows, hardcoded_ply)
log_fitness([adaptive_ply, hybrid_ply], fitness)

logging.info("Evolving players... [takes a little]")
evaluator = partial(scalar_evaluator, fitness = fitness) 
adaptive_ply, _ = one_lambda(adaptive_ply, 5, evaluator, 100) 
hybrid_ply, _ = one_lambda(hybrid_ply, 5, evaluator, 100)
logging.info("after evolution")
log_fitness([adaptive_ply, hybrid_ply], fitness)

logging.info("Train hybrid player with lexicase selection against")
adversaries = [hardcoded_ply, good_ply, random_ply]
logging.info(f"({', '.join((ply.__name__ for ply in adversaries))})")
adv_games = [20, 20, 20]
player = HybridPly(rows, hardcoded_ply)

fitness = partial(lexicase_nim_fitness, adversaries=adversaries, rows = rows, n_games = adv_games)
evaluator = partial(lexicase_evaluator, fitness = fitness, fit_dimensions = len(adversaries))

logging.info(f"Initial Fintess: {fitness(player, n_games=len(adversaries)*[simulations])}")
logging.info("Evolving player... [takes a little]")
_, history = one_lambda(player, 5, evaluator, 100)

def is_pareto(costs: list) -> list:
    is_efficient = len(costs) * [True]
    compare_costs = lambda a, b: any(a_i > b_i for a_i, b_i in zip(a, b))
    for i, a in enumerate(costs):
        is_efficient[i] = all(compare_costs(a, b) for b in costs if b != a)
    return is_efficient

_, players = zip(*history)
fitnesses = [fitness(p, n_games=len(adversaries)*[simulations]) for p in players]
pareto_fitnesses = (f for f, b in zip(fitnesses, is_pareto(fitnesses)) if b)

logging.info("Select a player form the Pareto bound")
for i, fit in enumerate(pareto_fitnesses):
    logging.info(f" - Player {i} has fitness {tuple('%.2f' % f for f in fit)}")

index = int(input("Select a player to play against:"))
best = players[i]
print(lexicase_nim_fitness(best, adversaries=adversaries, rows = rows, n_games = len(adversaries)*[simulations]))


logging.info("You will now play 2 matches against the selected player")
logging.info("| You start first |")
Duel(Nim(rows), human_ply, best, visible = True).play()
logging.info("| You start second |")
Duel(Nim(rows), best, human_ply, visible = True).play()

