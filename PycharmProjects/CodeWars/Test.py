def recSubPlotDet(plotNumber:int):
    n=plotNumber
    factors=[]
    i=2
    while(n!=1): # feed factors arr with factors 18 = [2,3,3]
       if n%i==0:
           factors.append(i)
           n/=i
       else:
           i+=1

    if len(factors)==1: # we need a rectangular subplot, so 3*1 is not enough -> 2*2
        return recSubPlotDet(plotNumber+1)
    if len(factors)>2:
        i=0
        while(len(factors)!=2):
            factors[i%2]*=factors[-1]
            i+=1
            factors.pop(-1)
    if(factors[1]<factors[0]): # if width < high swap them
        return factors[1], factors[0]
    return factors[0], factors[1]





print(recSubPlotDet(20))