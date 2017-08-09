import time
def whoIsNext(names : list, r : int) -> str:
    i=0
    while(5*(2**i)<r):
        i+=1
    if(i>0):
        r-=5*(2**(i-1))
    else:
        return names[r-1]
    position=1
    while(1):
        if(r<position*(2**(i-1))):
            break
        position+=1
    return names[position-1]


names = ["Sheldon", "Leonard", "Penny", "Rajesh", "Howard"]


print(whoIsNext(names,1000000000))

