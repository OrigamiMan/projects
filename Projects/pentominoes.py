from typing import Tuple, List
from pprint import pprint
from time import sleep

pentos = {
    "F": (
        (0, 1, 1),
        (1, 1, 0),
        (0, 1, 0)
    ),
    
    "G": (
        (1, 1, 0),
        (0, 1, 1),
        (0, 1, 0)
    ),
    
    "I": (
        (1),
        (1),
        (1),
        (1),
        (1)
    ),
}


def get_size(s: str) -> Tuple[int]:
    w = len(pentos[s][0])
    h = len(pentos[s])
    return (w, h)

def blit(dest: List[List[int]], shape: str, pos: Tuple[int], n: int) -> None:
    sw, sh = get_size(shape)
      
    for y in range(sh):
        for x in range(sw):
            px, py = x+pos[0], y+pos[1]
            if dest[py][px] != 0:
                raise Exception()
            if pentos[shape][y][x] != 0:
                dest[py][px] = n
            
def get_neighbors(surface: List[List[int]], coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = coord
    candidates = (
        (x, y + 1),
        (x, y - 1),
        (x + 1, y),
        (x - 1, y)
    )
    neighbors = []
    for cx, cy in candidates:
        if cx < 0 or cx >= len(surface[0]):
            continue 
        if cy < 0 or cy >= len(surface):
            continue
        neighbors.append((cx, cy))
    
    return neighbors
    
def combi_id(surface: List[List[int]]) -> Tuple[Tuple[int]]:
    result = [row for row in surface if set(row) != {0, }]
    
    leftmost_idx = len(result[0])
    rightmost_idx = 0
    
    for row_idx in range(len(result)):
        for col_idx in range(len(result[row_idx])):
            value = result[row_idx][col_idx]
            if value != 0 and leftmost_idx > col_idx:
                leftmost_idx = col_idx
            if value != 0 and rightmost_idx < col_idx:
                rightmost_idx = col_idx
    
    result = [row[leftmost_idx:rightmost_idx + 1] for row in result]   
    result = [[-1 if item != 0 else 0 for item in row] for row in result]
        
    return tuple([tuple(row) for row in result])
    


def connected(surface: List[List[int]]) -> bool:
    for y in range(len(surface)):
        for x in range(len(surface[y])):
            if surface[y][x] == 0:
                continue 
            cur_value = surface[y][x]
            for nx, ny in get_neighbors(surface, (x, y)):
                n_value = surface[ny][nx]
                if n_value > 0 and n_value != cur_value:
                    return True 
    return False

def print_combi(surface: List[list[int]]) -> None:
    for line in surface:
        if 0 in line and len(set(line)) == 1:
            continue
        to_print = ""
        for n in line:
            if n == 0: to_print += "⬛"
            elif n == 1: to_print += "🟦"
            elif n == -1: to_print += "🔳"
            else: to_print += "⬜"
        
        print(to_print)

def combi(s1: str, s2: str) -> int:
    s1_w, s1_h = get_size(s1)
    s2_w, s2_h = get_size(s2)
    
    surface_w, surface_h = 2 * s1_w + s2_w, 2 * s1_h + s2_h
    combinations = set()
    counter = 1
    for px in range(surface_w - s1_w + 1):
        for py in range(surface_h - s1_h + 1):
            try:
                surface = [[0 for h in range(surface_w)] for h in range(surface_h)]
                blit(surface, s1, (px, py), 1)
                blit(surface, s2, (s1_w, s1_h), 2)
                if connected(surface):
                    comb_id = combi_id(surface)
                    #if comb_id not in combinations:
                    print_combi(surface)
                    print_combi(comb_id)
                    combinations.add(comb_id)
                    print(counter)
                    counter += 1
            except Exception:
                continue
    return len(combinations)
            

    

    
assert combi("F", "F") == 7