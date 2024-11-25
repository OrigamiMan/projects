from math import gcd

def promenade(sequence: str):
    l_index = sequence.rfind("L")
    r_index = sequence.rfind("R")
    if l_index == -1:
        l_value = (1, 0)
    else:
        l_value = promenade(sequence[:l_index])
        
    if r_index == -1:
        r_value = (0, 1)
    else:
        r_value = promenade(sequence[:r_index])

    divisor = gcd(l_value[0] + r_value[0], l_value[1] + r_value[1])
    return (int((l_value[0] + r_value[0])/divisor), int((l_value[1] + r_value[1])/divisor))

print(promenade("L"))
print(promenade("R"))
print(promenade("LRLL"))
print(promenade("LLRLR"))
print(promenade("LLLRRR"))
print(promenade("LLRRLL"))
print(promenade("RRRLRRR"))
print(promenade("LLLLRLLLL"))
print(promenade("LLLLLLLLLL"))
print(promenade("LRLRLRLRLR"))
