from typing import Tuple, List
from pprint import pprint


pentaminoes = {
    "F": (
        (0, 1, 1),
        (1, 1, 0),
        (0, 1, 0),
    ),
    "X": (
        (0, 1, 0),
        (1, 1, 1),
        (0, 1, 0),
    ),
    "V": (
        (1, 0, 0),
        (1, 0, 0),
        (1, 1, 1),
    ),
}


def get_size(s: str) -> Tuple[int]:
    return len(pentaminoes[s][0]), len(pentaminoes[s])


def blit(dest: List[List[int]], shape: str, pos: Tuple[int], n: int) -> None:
    sw, sh = get_size(shape)

    for y in range(sh):
        for x in range(sw):
            py, px = y + pos[1], x + pos[0]
            if dest[py][px] != 0 and pentaminoes[shape][y][x] != 0:
                raise Exception("Occupied!")
            if pentaminoes[shape][y][x] != 0:
                dest[py][px] = n


def combination_id(surface: List[List[int]]) -> Tuple[Tuple[int]]:
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
    result = [[-1 if item > 0 else 0 for item in r] for r in result]
    return tuple([tuple(row) for row in result])


def get_neighbors(surface: List[List[int]], coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = coord
    candidates = (
        (x, y + 1),
        (x - 1, y),
        (x, y - 1),
        (x + 1, y)
    )
    neighbors = []
    for cx, cy in candidates:
        if cx < 0 or cx >= len(surface[0]):
            continue
        if cy < 0 or cy >= len(surface):
            continue
        neighbors.append((cx, cy))
    return neighbors


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


def print_combination(surface: List[List[int]]) -> None:
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
    print("")


def combinations(s1: str, s2: str) -> int:
    s1w, s1h = get_size(s1)
    s2w, s2h = get_size(s2)

    sw = 2 * s1w + s2w
    sh = 2 * s1h + s2h
    counter = 1
    combinations = set()
    for py in range(sh - s1h + 1):
        for px in range(sw - s1w + 1):
            try:
                surface = [[0 for _ in range(sw)] for _ in range(sh)]
                blit(surface, s1, (px, py), 1)
                blit(surface, s2, (s1w, s1h), 2)
                if connected(surface):
                    comb_id = combination_id(surface)
                    if comb_id not in combinations:
                        print(counter)
                        print_combination(surface)
                        counter += 1
                    combinations.add(comb_id)
            except Exception:
                continue
    return len(combinations)


test_surface = [[0, 0, 0] for i in range(3)]
assert get_neighbors(test_surface, (0, 0)) == [(0, 1), (1, 0)]


assert combinations("F", "F") == 7
assert combinations("X", "X") == 6