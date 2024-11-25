from pprint import pprint


board = [["." for _ in range(10)] for _ in range(10)]

def x_y_r(a, c, m, r):
    coords = (a*r + c) % m
    x, y = coords % 10, coords // 10
    new_r = (a*coords + c) % m
    return (x, y, new_r)


def place_ship(a, c, m, r, n: int):
    x, y, r = x_y_R