from math import sqrt


def math_fib(n: int) -> int:
    return ((((1 + sqrt(5))/2) ** n) - (((1 - sqrt(5))/2) ** n))/sqrt(5)

cache = {
    0:1,
    1:1
}

def fib(n: int) -> int:
    if n not in cache:
        cache[n] = fib(n-1) + fib(n-2)
    return cache[n]

for i in range(100):
    print(round(math_fib(i)))
    
for i in range(99):
    print(fib(i))

assert fib(0) == 1
assert fib(1) == 1
assert fib(2) == 2
assert fib(5) == 8