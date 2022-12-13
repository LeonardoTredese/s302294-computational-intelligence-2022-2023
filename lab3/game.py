import logging
from collections import namedtuple
from typing import Callable, Generator
from copy import deepcopy

Nimply = namedtuple("Nimply", "row, num_objects")

class Nim:
    def __init__(self, num_rows: int) -> None:
        self._rows = [i*2 + 1 for i in range(num_rows)]

    def nimming(self, ply: Nimply) -> None:
        assert self._rows[ply.row] >= ply.num_objects
        self._rows[ply.row] -= ply.num_objects
    
    def __bool__(self) -> bool:
        return sum(self._rows) > 0

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def __str__(self) -> str:
        out = ""
        for i, row in enumerate(self._rows):
            out += f"{i} {(len(self._rows) - i) * ' '} {row * '*'}\n"
        return out

class Duel:
    def __init__(self, game: Nim, player0: Callable, player1: Callable, visible: bool = False) -> None:
        self._game = game
        self._players  = [player0, player1]
        self._turn = 0
        self._visible = visible

    def log(self, message: str) -> None:
        if self._visible:
            logging.info(message)
        else:
            logging.debug(message)

    def play(self) -> int:
        while self._game:
            player = self._players[self._turn]
            self.log(f"Player {player.__name__} turn")
            self.log(self._game)
            ply = player(self._game)
            self._game.nimming(ply)
            self._turn = 1 - self._turn
        self.log(f"Player {player.__name__} won")
        return 1 - self._turn 

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

    def possible_plies(self) -> Generator:
        return (Nimply(r, o) for r, m in enumerate(self._rows) for o in range(1, m+1))

    def __bool__(self) -> bool:
        return sum(self._rows) > 0

    def __hash__(self) -> int:
        return self._rows.__hash__()

    def __eq__(self, other) -> bool:
        return self._rows == other.rows 

    @property
    def rows(self) -> tuple:
        return tuple(self._rows)

    def __str__(self) -> str:
        out = ""
        for i, row in enumerate(self._rows):
            out += f"{i} {row * '*'}\n"
        return out

    def __repr__(self) -> str:
        return "NimNode" + str(self._rows) 

def game_node_mapping(game: Nim) -> list:
    game_node_map = sorted(((o, i) for i, o in enumerate(game.rows) if o))
    _, row_map = zip(*game_node_map)
    return row_map
