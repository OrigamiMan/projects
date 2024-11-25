from typing import List
from math import inf


def buttom_up_cut_rod(length: int, prices: List[int]) -> int:
    r = [None for _ in range(length + 1)]
    r[0] = 0
    for j in range(1, length + 1):
        q = -inf
        for i in range(1, j + 1):
            q = max(q, prices[i] + r[j - i])
        r[j] = q
    return r[length]

prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]    
    
assert buttom_up_cut_rod(4, prices) == 10
    
    