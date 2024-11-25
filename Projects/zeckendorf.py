from typing import List

cache = [1, 1]


def zeckendorf(n: int) -> List[int]:
    if n in cache:
        return [n]
    
    while cache[-1] <= n:
        cache.append(cache[-1] + cache[-2])
        
    result = []
    while n > 0:
        for i in range(len(cache)):
            if cache[i+1] > n:
                result.append(cache[i])
                n -= cache[i]
                break
            
    return result
        


assert zeckendorf(100) == [89, 8, 3]
assert zeckendorf(832040) == [832040]
assert zeckendorf(1) == [1]
assert zeckendorf(514228) == [317811, 121393, 46368, 17711, 6765, 2584, 987, 377, 144, 55, 21, 8, 3, 1]