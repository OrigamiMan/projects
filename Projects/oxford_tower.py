from typing import Tuple, Set
from pprint import pprint
from time import time

def from_string(state: str) -> Tuple[Tuple[str]]:
    pegs = state.split(" ")
    result = tuple()
    for peg in pegs: 
        if peg == "0":
            result += (tuple(), )
            continue
        result += (tuple(el for el in peg), )
    return result
            
def possible_moves(state: Tuple[Tuple[int]]) -> Set[Tuple[Tuple[str]]]:
    result = set()
    
    for peg_id in range(len(state)):
        if len(state[peg_id]) == 0:
            continue
        lstate = [[p for p in peg] for peg in state]
        element = lstate[peg_id].pop()
        for i in range(len(state)):
            if peg_id == i:
                continue
            lstate_copy = [[p for p in peg] for peg in lstate]
            lstate_copy[i].append(element)
            result.add(tuple(tuple(i) for i in lstate_copy))
    return result    

def moves(state1: str, state2: str) -> int:
    state1 = from_string(state1)
    state2 = from_string(state2)
    
    queue = [(state1, 0)]
    visited = set()

    while queue:
        current_state, m = min(queue, key=lambda e: e[1])
        queue.remove((current_state, m))
        if current_state == state2: 
            return m
        visited.add(current_state)
        for s in possible_moves(current_state):
            if s in queue or s in visited:
                continue
            queue.append((s, m + 1))

    
    pprint(possible_moves(state1))
    
    

assert moves("12 0 3 4", "1 32 4 0") == 3
assert moves("12 0 34 0", "12 0 34 0") == 0
assert moves("1 23 0 4", "1 2 3 4") == 1
time1 = time()
assert moves("1234 0 0 0", "4321 0 0 0") == 9
time2 = time()

print(time2 - time1)