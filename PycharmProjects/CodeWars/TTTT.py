x=[1,1,1,4,5,6]
while (1):
    try:
        x.remove(1)
    except(ValueError):
        break
print(x)