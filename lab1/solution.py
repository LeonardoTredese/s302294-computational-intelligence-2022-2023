from gx_utils import *
import numpy as np
import logging
import random
from typing import Callable, Generator

logging.basicConfig(format="%(message)s", level=logging.INFO)

RANDOM_SEED = 42
PROBLEM_SIZE = [5, 10, 20, 100, 500, 1000] 

def problem(N: int, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

def search(
    initial_state: frozenset,
    goal_test: Callable,
    possible_actions: Callable,
    state_cost: dict, 
    priority_function: Callable,
    unit_cost: Callable,
):
    frontier = PriorityQueue()
    state_cost.clear()

    state = initial_state
    state_cost[state] = 0

    while state is not None and not goal_test(state):
        for a in possible_actions(state):
            new_state = result(state, a)
            cost = unit_cost(a)
            if new_state not in state_cost and new_state not in frontier:
                state_cost[new_state] = state_cost[state] + cost
                frontier.push(new_state, p=priority_function(new_state))
                logging.debug(f"Added new node to frontier (cost = {state_cost[new_state]})")
        if frontier:
            state = frontier.pop()
        else:
            state = None
    return state

def gen_goal_test(N: int) -> Callable:
    """Return a function that tests the goal for the problem of size N"""
    GOAL = set(range(N)) 
    def goal_test(state: frozenset) -> bool:
        """Test if the state contains all numbers in [0, N-1]"""
        different_numbers = set()
        reached_goal = False
        for list_ in state:
            different_numbers.update(list_)
            reached_goal = different_numbers == GOAL
            if reached_goal:
                break
        return reached_goal
    return goal_test


def gen_possible_actions(problem_input: list) -> Callable:
    """
        Returns a function that generates all the possible actions
        for problem_input
    """
    PROBLEM = sorted(set(map(lambda x: tuple(x), problem_input)))
    def possible_actions(state: frozenset) -> Generator[int, None, None]:
        """
           Returns a generator that outputs all the possible
           actions from the given state 
        """
        return (list_ for list_ in PROBLEM if list_ not in state)
    return possible_actions


def result(state: frozenset, action: tuple) -> frozenset:
    return state.union([action])

def gen_h(N: int) -> Callable:
    """Returns a heuristic function for the problem of size N"""
    def h(state: frozenset()) -> int:
        """
            Returns the number of missing elements to the current state.
            This heuristic is optimistic since you cannot reach a final
            state with less than the number of missing elements.
        """
        different_numbers = set()
        for list_ in state:
            different_numbers.update(list_)
            if len(different_numbers) == N:
                break
        return N - len(different_numbers)
    return h

INITIAL_STATE = frozenset()
state_cost = dict()


for n in PROBLEM_SIZE:
    problem_ = problem(n, seed=RANDOM_SEED)

    def dijkstra(state: frozenset) -> int:
        return state_cost[state]

    def A_star(state: frozenset) -> int:
        heuristic = gen_h(n)
        return dijkstra(state) + heuristic(state)

    for priority_function in [A_star, dijkstra]:
        logging.info(f"Starting search for N: {n:,} with {priority_function.__name__}:")
        final = search(
            INITIAL_STATE,
            goal_test=gen_goal_test(n),
            possible_actions=gen_possible_actions(problem_),
            state_cost=state_cost,
            priority_function=priority_function,
            # size of added list is the unit cost
            unit_cost=len,
        )
        logging.info(f"\tFound a solution with cost {state_cost[final]}\n\tvisited {len(state_cost):,} states")
