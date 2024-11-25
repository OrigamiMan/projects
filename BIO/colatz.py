queue = {4}
checked = {1, 2}

def get_previous(n: int):
    if n*2 not in checked:
        queue.add(n*2)
    if (n-1)%3 == 0 and (n-1)%3 not in checked:
        queue.add((n-1)/3)
        

