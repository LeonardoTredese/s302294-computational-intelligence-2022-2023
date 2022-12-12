import logging
from collections import namedtuple
from typing import Callable

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

