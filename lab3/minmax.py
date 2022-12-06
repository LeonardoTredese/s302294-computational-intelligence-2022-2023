import logging
from collections import namedtuple
from functools import cache
from game import Nim, Nimply, Duel
from players import top_ply, human_ply
from copy import deepcopy

logging.basicConfig(format="%(message)s", level=logging.INFO)

class NimNode:
    """ Compact hashable representation of the nim game """
    def __init__(self, num_rows: int = 3, game: Nim = None) -> None:
        if game is None:
            self._rows = tuple(i*2 + 1 for i in range(num_rows))
        else:
            self._rows = tuple(sorted((o for o in game.rows if o)))

    def nimming(self, ply: Nimply):
        assert self._rows[ply.row] >= ply.num_objects
        next_game = deepcopy(self)
        next_rows = next_game._rows[:ply.row] + (next_game._rows[ply.row] - ply.num_objects,) + next_game._rows[ply.row+1:] 
        next_rows = tuple(sorted((o for o in next_rows if o)))
        next_game._rows = next_rows
        return next_game
    
    def __bool__(self) -> bool:
        return sum(self._rows) > 0

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def __str__(self) -> str:
        out = ""
        for i, row in enumerate(self._rows):
            out += f"{i} {row * '*'}\n"
        return out

@cache
def nim_min_max(node: NimNode, turn: str = 'min') -> int:
    if not node:
        return (-1, None) if turn == 'max' else (1, None) 
    moves = sorted((Nimply(r, o) for r, m in enumerate(node.rows) for o in range(1, m+1)), key=lambda x: x.num_objects, reverse=True)
    outcomes = ((nim_min_max(node.nimming(move), 'min' if turn=='max' else 'max'), move) for move in moves)
    for (next_outcome, prev_move), move in outcomes:
        if turn == 'max' and next_outcome == 1:
            return 1, move
        elif turn == 'min' and next_outcome == -1:
            return -1, move
    return (-1, move) if turn == 'max' else (1, move)

def minmax_ply(game: Nim) -> Nimply:
    # deal with compact notation
    game_node_map = sorted(((o, i) for i, o in enumerate(game.rows) if o))
    _, row_map = zip(*game_node_map)
    _, ply = nim_min_max(NimNode(game=game), 'min')
    return Nimply(row_map[ply.row], ply.num_objects)

game = Nim(4)
# Games starts with nim sum 0 so top_ply cannot win against minmax_ply
Duel(game, top_ply, minmax_ply, visible=True).play()

game = Nim(4)
Duel(game, minmax_ply, human_ply, visible=True).play()
