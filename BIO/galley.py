from math import factorial

def number_of_arrangements(a: int, b: int, c: int, d: int):
    return int(factorial(a+b+c+d)/(factorial(a) * factorial(b) * factorial(c) * factorial (d)))


def find_arrangement(a: int, b: int, c: int, d: int, n: int):
    if a-1 >= 0:
        start_with_a = number_of_arrangements(a-1, b, c, d)
        if n <= start_with_a:
            first_letter = "A"
            other_letters = find_arrangement(a-1, b, c, d, n)
            if other_letters:
                return first_letter + other_letters
            return first_letter
        n -= start_with_a
        
    if b-1 >= 0:
        start_with_b = number_of_arrangements(a, b-1, c, d)
        if n <= start_with_b:
            first_letter = "B"
            other_letters = find_arrangement(a, b-1, c, d, n)
            if other_letters:
                return first_letter + other_letters
            return first_letter
        n -= start_with_b
        
    if c-1 >= 0:
        start_with_c = number_of_arrangements(a, b, c-1, d)
        if n <= start_with_c and c-1 >= 0:
            first_letter = "C"
            other_letters = find_arrangement(a, b, c-1, d, n)
            if other_letters:
                return first_letter + other_letters
            return first_letter
        n -= start_with_c
    
    if d-1 >= 0:
        first_letter = "D"
        other_letters = find_arrangement(a, b, c, d-1, n)
        if other_letters:
            return first_letter + other_letters
        return first_letter

print(find_arrangement(1, 2, 1, 0, 8))
print(find_arrangement(1, 0, 0, 0, 1))
print(find_arrangement(1, 1, 0, 0, 2))
print(find_arrangement(0, 3, 0, 3, 12))
print(find_arrangement(5, 5, 0, 0, 56))
print(find_arrangement(2, 2, 2, 2, 2520))
print(find_arrangement(2, 3, 4, 5, 1234567))
print(find_arrangement(5, 4, 4, 4, 123456789))
print(find_arrangement(5, 5, 5, 5, 11223344556))
