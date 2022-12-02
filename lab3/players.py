import random
import logging
import numpy as np
from functools import reduce
from operator import xor
from game import Nim, Nimply
from evolved_agents import SelfAdaptiveParameters

def dumb_ply(game: Nim) -> Nimply:
    n_objects, idx = max((o, r) for r, o in enumerate(game.rows))
    return Nimply(idx, n_objects)

def good_ply(game: Nim) -> Nimply:
    nim_sum = reduce(xor, game.rows)
    if nim_sum:
        n_objects, row = max(((o & nim_sum, r) for r, o in enumerate(game.rows)))
    else:
        row = next((r for r, o in enumerate(game.rows) if o))
        n_objects = 1
    return Nimply(row, n_objects)

def top_ply(game: Nim) -> Nimply:
    sum_zero_ply = None
    nim_sum = reduce(xor, game.rows)
    row, objects = next(((r, o - xor(o, nim_sum)) for r, o in enumerate(game.rows) if xor(o, nim_sum) < o), (None, None))
    if row is None:
        row = next((r for r, o in enumerate(game.rows) if o))
        objects = 1
    return Nimply(row, objects)

def terrible_ply(game: Nim) -> Nimply:
    best_ply = top_ply(game)
    elems = game.rows[best_ply.row]
    return Nimply(best_ply.row, min(best_ply.num_objects + 1, elems))

def human_ply(game: Nim) -> Nimply:
    row, num_objects = input("Insert move: ").split()
    return Nimply(int(row), int(num_objects))

def random_ply(game: Nim) -> Nimply:
    row = random.choice([i for i, o in enumerate(game.rows) if o])
    n_objects = random.randint(1, game.rows[row])
    return Nimply(row, n_objects)

class AdaptiveRule:
    def __init__(self, params: SelfAdaptiveParameters , row: int) -> None:
        self._weight = params[0]
        self._bias = params[1]
        self._objects = params[2]
        self._params = params
        self._row = row
   
    def tweak(self):
        new_params = self._params.tweak()
        return AdaptiveRule(new_params, self._row)    

    def activation(self, game: Nim) -> float:
        row_elems = game.rows[self._row]
        return int(row_elems > 0) * max(self._weight * row_elems + self._bias, 0)

    def action(self, game: Nim) -> Nimply:
        row_elems = game.rows[self._row]
        objects = round(self._objects)
        return Nimply(self._row, min(max(objects, 1), row_elems))

class AdaptivePlayer:
    def __init__(self, n_rows: int, rules: list = None) -> None:
        self.__name__ = "AdaptivePlayer"
        if rules is None:
            rules_init = ((SelfAdaptiveParameters(10 * np.random.random(3), 10 * np.random.random(3)), row) for row in range(n_rows) for _ in range(10))
            self._rules = [AdaptiveRule(*ri) for ri in rules_init]
        else:
            self._rules = rules
        self._n_rows = n_rows

    def tweak(self):
        new_rules = [rule.tweak() for rule in self._rules]
        return AdaptivePlayer(self._n_rows, rules=new_rules)

    def __call__(self, game: Nim) -> Nimply:
        rule = max(self._rules, key= lambda r: r.activation(game)) 
        return rule.action(game)
            
        
            
