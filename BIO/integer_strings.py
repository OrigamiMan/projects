start, n = input().split(" ")

power = len(start)
n = int(n)
start = int(start)

until_next_power = power*(10**power - start)

while n - until_next_power > 0:
    n -= until_next_power
    start = 10**power
    power += 1
    until_next_power = power*(10**power - start)

num, r = n // power, n % power

if r == 0:
    num -= 1
    
print(str(start + num)[r-1])