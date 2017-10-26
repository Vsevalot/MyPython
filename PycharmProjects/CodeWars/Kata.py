def find_all(sum_dig, digs):
    print(sum_dig,digs)
    if(sum_dig<digs):
        return []
    final = 10 ** digs
    start=10**(digs-1)
    v=sum_dig
    z=[0]*digs
    i=digs
    while(i>-1):
        if(v-9>0):
            z[i-1]=9
            v-=9
        else:
            if(i==1):
                z[0]=v
                break
            for k in range(len(z)):
                if z[k]==0:
                    z[k]=1
            z[i-1]=v-i+1
            break
        i-=1
    start=int(''.join([str(v) for v in z]))
    if sum_dig//digs<9:
        final = int((str((sum_dig // digs)+1))*digs)
    elif sum_dig//digs>9:
        return []
    numbers=[x for x in range(start,final,1) if (sum([int(n) for n in str(x)])==sum_dig) and ''.join(sorted([n for n in str(x)]))==str(x)]
    return [len(numbers),numbers[0],numbers[-1]]

print(find_all(35, 6))