import random
from copy import deepcopy
from collections import defaultdict
from typing import Callable
from game import Nim, Nimply, Duel
from minmax import NimNode, game_node_mapping, nim_min_max



class NimRLAgent:
    def __init__(self, alpha: float = 0.15, gamma: float = 0.8, explore_rate: float = 0.2) -> None:
        self.__name__ = "rl_ply"
        self._history = [] # state, move
        self._weight = alpha
        self._discount = gamma
        self._explore_rate = explore_rate
        self._quality = defaultdict(random.random)
        self._training = True

    def __call__(self, game: Nim) -> Nimply:
        state = NimNode(game = game)
        row_map = game_node_mapping(game)
        possible_plies = state.possible_plies() 
        if self._explore_rate >= random.random() and self._training:
            ply = random.choice(list(possible_plies))
        else:
            ply = max(possible_plies, key = lambda p: self._quality[(state, p)])
        if self._training:
            self._history.append((state, ply))
        return Nimply(row_map[ply.row], ply.num_objects)
    
    def learn(self, has_won: bool) -> None:
        for state, ply in reversed(self._history):
            next_state = state.nimming(ply)
            curr_quality = self._quality[state, ply]
            reward = 1 if has_won else -1
            if next_state:
                next_quality = max(map(lambda p: self._quality[next_state, p], next_state.possible_plies()))
            else:
                next_quality = 1
            self._quality[state, ply] =  (1 - self._weight)*curr_quality + self._weight*(reward + self._discount*next_quality)
        self._history.clear()
        self._explore_rate -= 1e-5

class Trainer:
    def __init__(self, rows: int, adversary: Callable, agent: NimRLAgent = None) -> None:
        self._game_rows = rows
        self._adv = adversary
        self._agent = NimRLAgent() if agent is None else agent
        self._agent._training = True

    def train(self, episodes: int) -> NimRLAgent:
        for episode in range(episodes):
            game = Nim(self._game_rows)
            if episode % 2:
                duel = Duel(game, self._adv, self._agent)
                has_won = bool(duel.play())
            else:
                duel = Duel(game, self._agent, self._adv)
                has_won = not bool(duel.play())
            self._agent.learn(has_won)
        self._agent._training = False
        return self._agent

if __name__ == '__main__':
    import numpy as np
    from evolved_agents import nim_fitness
    from players import random_ply, hardcoded_ply, human_ply, good_ply
    rows = 4
    agent_ply = Trainer(rows, hardcoded_ply).train(10_000)
    print("Against hardcoded_ply", nim_fitness(agent_ply, adversary = hardcoded_ply, rows=rows, n_games = 1000))
    print("Against random_ply", nim_fitness(agent_ply, adversary = random_ply, rows=rows, n_games = 1000))
    print("Against good_ply", nim_fitness(agent_ply, adversary = good_ply, rows=rows, n_games = 1000))
    Duel(Nim(4), agent_ply, human_ply, visible=True).play()
  

    
        
 
               
            
        
