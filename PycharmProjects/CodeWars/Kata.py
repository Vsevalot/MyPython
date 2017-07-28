def iq_test(numbers):
    arr=numbers.split()
    comp=[0,0]
    for i in range(len(arr)):
        if(int(arr[i])%2==0):
            comp[0]+=1
            if(comp[0]>1):
                return 
        else:
            comp[1]+=1


a="2 4 7 8 10"
print(iq_test(a))

a="1 2 2"
print(iq_test(a))