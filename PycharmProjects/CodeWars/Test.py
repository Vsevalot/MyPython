import datetime

def matName2Time(matName: str) -> [datetime.date,datetime.time]: # convert Mat file's name to date and time
    opening=matName.index('(')
    closing=matName.index(')')
    timeDelta=30*int(matName[opening+1:closing])
    matName=matName[:opening]
    t=datetime.timedelta(hours=int(matName[-12:-10]), minutes=int(matName[-9:-7]), seconds=int(matName[-6:-4])+timeDelta)
    d=datetime.date(int(matName[-21:-17]),int(matName[-17:-15]), int(matName[-15:-13]))+t
    m,s=divmod(t.seconds, 60)
    h,m=divmod(m, 60)
    t=datetime.time(h,m,s)
    return d,t

a='20091231_23.59.20.mat(3)'

print(a[:8])