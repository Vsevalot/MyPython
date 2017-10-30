CHARS ="0123456789"+"ABCDEFGHIGKLMNOPQRSTUVWXYZ"+"ABCDEFGHIGKLMNOPQRSTUVWXYZ".lower()
def is_polydivisible(s, b):
    if(b==10):
        for i in range(len(s)):
            if int(s[:i+1])%(i+1)!=0:
                return False
            return True
    return is_polydivisible(sum([CHARS.index(s[i])*b**(i) for i in range(len(s)-1,-1,-1)]),10)


def get_polydivisible(n, b):
    i=0
    poly=[]
    while(len(poly)<n):
        if(is_polydivisible(str(i),10)):
            poly.append(i)
        i+=1
    x=poly[-1]

