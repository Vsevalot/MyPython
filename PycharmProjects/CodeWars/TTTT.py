def find_next_square(sq):
    from math import sqrt
    a=sqrt(sq)
    try:
        a=int(a)
        return (a+1)*(a+1)
    except:
        return -1

