from math import sqrt, ceil

def E(i: int):
    return 2*i  

def O(i: int):
    return 2*i - 1

def T(i: int):
    return ceil((sqrt(8*i+1)-1)/2)

def combine(left, right):
    
    def s3(i: int):
        return right(left(right(i)))
    return s3

def mass_combine(string: str):
    final = None
    to_combine = None
    skip_letters = 0
    for id in range(len(string)):
        if skip_letters != 0:
            skip_letters -= 1
            continue
        
        letter = string[id]
        if letter == "E":
            to_combine = E
        elif letter == "O":
            to_combine = O
        elif letter == "T":
            to_combine = T
        elif letter == "(":
            
            bracket_power = 1
            sub_string = string[id+1:]
            for j in range(len(sub_string)):     
                if sub_string[j] == "(":
                    bracket_power += 1    
                elif sub_string[j] == ")":
                    bracket_power -= 1  
                    
                if bracket_power == 0:
                    to_combine = mass_combine(string[id+1:id+1+j])
                    break
                
            last_bracket_id = string.rfind(")")
            skip_letters = last_bracket_id - id
                
        if final is None:
            final = to_combine
            continue
        final = combine(final, to_combine)
    return final
        
        
mc = mass_combine("EE(O(EEEE))O")  
print(mc(12345678))