import logging
from collections import namedtuple
from functools import cache
from game import Nim, Nimply, Duel, NimNode, game_node_mapping
from players import top_ply, human_ply

logging.basicConfig(format="%(message)s", level=logging.INFO)

@cache
def nim_min_max(node: NimNode, turn: str = 'min') -> int:
    if not node:
        return (-1, None) if turn == 'max' else (1, None) 
    moves = sorted(node.possible_plies(), key=lambda x: x.num_objects, reverse=True)
    outcomes = ((nim_min_max(node.nimming(move), 'min' if turn=='max' else 'max'), move) for move in moves)
    for (next_outcome, prev_move), move in outcomes:
        if turn == 'max' and next_outcome == 1:
            return 1, move
        elif turn == 'min' and next_outcome == -1:
            return -1, move
    return (-1, move) if turn == 'max' else (1, move)

def minmax_ply(game: Nim) -> Nimply:
    row_map = game_node_mapping(game)
    _, ply = nim_min_max(NimNode(game=game), 'min')
    return Nimply(row_map[ply.row], ply.num_objects)

if __name__ == '__main__':
    game = Nim(5)
    Duel(game, minmax_ply, top_ply, visible=True).play()
