from typing import List


def kill(h: int, t: int) -> List[str]:
    result = []
    #print(h, t)
    if h % 2 == 1:
        if t % 4 == 0:
            h, t = strike(h, t, "T")
            result.append("T")
        if t % 4 == 1:
            h, t = strike(h, t, "T")
            result.append("T")
        if t % 4 == 2:
            h, t = strike(h, t, "TT")
            result.append("TT")
        if t % 4 == 3:
            h, t = strike(h, t, "H")
            result.append("H")
            
    while h % 2 == 0 and t % 4 != 0:
        h, t = strike(h, t, "T")
        result.append("T")
    
    while t:
        h, t = strike(h, t, "TT")
        result.append("TT")
    while h:
        h, t = strike(h, t, "HH")
        result.append("HH")
            
    
    return h, t, result


def strike(h: int, t: int, s: str):
    if s == "T" and t >= 1:
        t -= 1
        t += 2
    if s == "TT" and t >= 2:
        t -= 2
        h += 1
    if s == "H" and h >= 1:
        h -= 1
        t += 1
    if s == "HH" and h >= 2:
        h -= 2
    #print(h, t)
    return h, t


for i in range(100):
    for j in range(100):
        h, t, result = kill(i+1, j+1)
        assert len(result) <= 1000 and h == 0 and t == 0
        



