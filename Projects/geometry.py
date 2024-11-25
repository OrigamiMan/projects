def on_segment(p, q, r):
    Xp, Yp = p
    Xq, Yq = q
    Xr, Yr = r
    conditions = (
        Xr < max(Xp, Xq),
        Xr > min(Xp, Xq),
        Yr < max(Yp, Yq),
        Yr > min(Yp, Yq),
    )

    return all(conditions)

def orientation(p, q, r):
    Xp, Yp = p
    Xq, Yq = q
    Xr, Yr = r

    coef = (Yq - Yp)*(Xr - Xq) - (Yr - Yq)*(Xq - Xp)

    if coef < 0:
        return -1
    elif coef > 0:
        return 1
    else:
        return 0

def intersect(p1, p2, w1, w2):
    o1 = orientation(p1, p2, w1)
    o2 = orientation(p1, p2, w2)
    o3 = orientation(w1, w2, p1)
    o4 = orientation(w1, w2, p2)
    
    conditions = (o1 != o2, o3 != o4)
    
    if all(conditions):
        return True

    if o1 == 0:
        return on_segment(p1, p2, w1)

    if o2 == 0:
        return on_segment(p1, p2, w2)
    
    if o3 == 0:
        return on_segment(w1, w2, p1)
    
    if o3 == 0:
        return on_segment(w1, w2, p2)

    return False

if __name__ == "__main__":      
    assert intersect((-150, 0), (150, 0), (0, -150), (0, 150)) == True