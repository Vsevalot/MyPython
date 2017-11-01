def sum_pairs(ints, s):
    candidats=[]
    plus=[]
    for i in range(len(ints)):
        delta=int(s)-ints[i]
        if delta in ints[i+1:]:
            candidats.append(i+1+ints[i+1:].index(delta))
        if len(candidats):
            if i==candidats[0]:
                break
    if len(candidats):
        return [int(s)-ints[min(candidats)],ints[min(candidats)]]
    return None




l= [10, 5, 2, 3, 7, 5]
print(l.index(5))
print(sum_pairs(l,'10'))