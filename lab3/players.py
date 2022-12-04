import random
import logging
import numpy as np
from functools import reduce, partial
from typing import Callable
from operator import xor
from game import Nim, Nimply
from evolved_agents import SelfAdaptiveParameters

def good_ply(game: Nim) -> Nimply:
    """ Faulty nim-sum implementation, takes nim-sum to zero only if it can remove a whole row  """
    nim_sum = reduce(xor, game.rows)
    if nim_sum:
        n_objects, row = max(((o & nim_sum, r) for r, o in enumerate(game.rows)))
    else:
        row = next((r for r, o in enumerate(game.rows) if o))
        n_objects = 1
    return Nimply(row, n_objects)

def top_ply(game: Nim) -> Nimply:
    """ nim-sum strategy """
    sum_zero_ply = None
    nim_sum = reduce(xor, game.rows)
    row, objects = next(((r, o - xor(o, nim_sum)) for r, o in enumerate(game.rows) if xor(o, nim_sum) < o), (None, None))
    if row is None:
        row = next((r for r, o in enumerate(game.rows) if o))
        objects = 1
    return Nimply(row, objects)

def human_ply(game: Nim) -> Nimply:
    """ Get ply from standard input """ 
    row, objects = input("Insert row and objects: ").split()
    return Nimply(int(row), int(objects))

def random_ply(game: Nim) -> Nimply:
    row = random.choice([i for i, o in enumerate(game.rows) if o])
    n_objects = random.randint(1, game.rows[row])
    return Nimply(row, n_objects)

def hardcoded_ply(game: Nim, default_ply: Callable = random_ply) -> Nimply:
    """ Try to apply a hardcoded behaviour otherwise use a default ply """ 
    non_null_rows = [(elems, i) for i, elems in enumerate(game.rows) if elems]
    if len(non_null_rows) == 1:
        elems, row = non_null_rows[0]
        return Nimply(row, elems)
    elif len(non_null_rows) == 2:
        max_elems, row = max(non_null_rows)
        min_elems, _ = min(non_null_rows)
        return Nimply(row, 1) if max_elems == min_elems else Nimply(row, max_elems - min_elems)
    elif sum(1 for e, _ in non_null_rows if e == 1) == len(non_null_rows) - 1:
        max_elems, row = max(non_null_rows)
        elems = max_elems if len(non_null_rows) % 2 else max_elems - 1
        return Nimply(row, elems)
    else:
        return default_ply(game)

class AdaptiveRule:
    """ Generic parametric rule """
    def __init__(self, row: int, params: SelfAdaptiveParameters = None) -> None:
        if params is None:
            n_params = 2 + 2*row+1
            self._params = SelfAdaptiveParameters(np.random.random(n_params), np.full(n_params, 1))
        else:
            self._params = params
        self._weight = self._params[0]
        self._bias = self._params[1]
        self._objects = self._params[2:]
        self._row = row
   
    def tweak(self):
        return AdaptiveRule(self._row, params = self._params.tweak())    

    def activation(self, game: Nim) -> tuple:
        """ Given a game returns a tuple inicating if its valid and its activation value """
        row_elems = game.rows[self._row]
        return row_elems > 0,  max(self._weight * row_elems + self._bias, 0)

    def action(self, game: Nim) -> Nimply:
        row_elems = game.rows[self._row]
        objects = int(1 + np.argmax(self._objects[:row_elems]))
        return Nimply(self._row, objects)

class AdaptivePly:
    """ Ply using only adaptive rules """
    def __init__(self, n_rows: int, rules: list = None) -> None:
        self.__name__ = "adaptive_ply"
        if rules is None:
            self._rules = [AdaptiveRule(row) for row in range(n_rows) for _ in range(row + 1)]
        else:
            self._rules = rules
        self._n_rows = n_rows

    def tweak(self):
        new_rules = [rule.tweak() for rule in self._rules]
        return AdaptivePly(self._n_rows, rules=new_rules)

    def __call__(self, game: Nim) -> Nimply:
        _, rule = max(((r.activation(game), r) for r in self._rules), key = lambda r: r[0])
        return rule.action(game)

class HybridPly:
    """ Ply using if possible hardcoded rules otherwise adaptive rules """
    def __init__(self, n_rows: int, algoritmic_ply: Callable, adaptive_ply: AdaptivePly = None) -> None:
        self.__name__ = "hybrid_ply"
        self._adaptive_ply = AdaptivePly(n_rows) if adaptive_ply is None else adaptive_ply
        self._algoritmic_ply = algoritmic_ply 
        self._ply = partial(algoritmic_ply, default_ply = self._adaptive_ply)
        self._num_rows = n_rows

    def tweak(self):
        return HybridPly(self._num_rows, self._algoritmic_ply, adaptive_ply = self._adaptive_ply.tweak())
    
    def __call__(self, game: Nim) -> Nimply:
        return self._ply(game) 
