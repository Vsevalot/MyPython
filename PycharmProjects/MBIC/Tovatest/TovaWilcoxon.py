import os
import sys

def mean_reaction_time(dictionary):
    M = 0
    n = 0
    for i in range(len(dictionary['rt'])):
        if ((dictionary['responded'][i] == 1) & (dictionary['corr'][i]==1)):
            M += dictionary['rt'][i]
            n += 1

    if n == 0:
        return -1  # if there is not any reaction time in the table
    else:
        return M / n

def xls2dict(path):
    table = []
    with open(path, "r") as myfile:
        for line in myfile:
            l = line.strip().split('\t')
            table.append(l)

    columns = []
    column = []
    table1 = []
    intline = []
    for i in range(1, len(table), 1):
        for k in range(len(table[i])):
            intline.append(int(table[i][k]))
        table1.append(intline)
        intline = []

    for k in range(len(table[0])):
        for i in range(len(table1)):
            column.append(table1[i][k])
        columns.append(column)
        column = []

    value_dict = {table[0][z]: columns[z] for z in range(len(table[0]))} # build a dictionary with titles of columns as keys
    return value_dict

def mistakes(dictionary):
    a=0
    n=0
    for i in range(len(dictionary['rt'])):
        if ((dictionary['corr'][i]==0) & (dictionary['responded'][i]==1)): # if patient pressed button without correct stimulus
            a+=1
        n=+1
    return a

def correct(dictionary):
    a=0
    n=0
    for i in range(len(dictionary['rt'])):
        if ((dictionary['corr'][i]==1) & (dictionary['responded'][i]==1)&(dictionary['targ'][i]==1)): # if patient pressed button with correct stimulus
            a+=1
        n=+1
    return a

def missed(dictionary):
    a=0
    n=0
    for i in range(len(dictionary['rt'])):
        if ((dictionary['corr'][i]==0) & (dictionary['responded'][i]==0)&(dictionary['targ'][i]==1)): # if patient missed correct stimulus
            a+=1
        n=+1
    return a

def bubble_sort(arr):
    for i in range(len(arr)):
        for k in range(len(arr)-1):
            if arr[k]>arr[k+1]: #swap
                a=arr[k]
                arr[k]=arr[k+1]
                arr[k+1]=a
    return arr

def moda(arr):
    if len(arr)%2==1:
        return arr[(len(arr)-1)/2]
    else:
        return arr[(len(arr))/2] + arr[len(arr)/2 - 1]

def wilcoxon(arr):
    dif = []
    moduls = []
    for i in range(len(arr[0])):
        dif.append(arr[0][i] - arr[1][i])
        if dif[i] < 0:
            moduls.append(dif[i] * -1)
        else:
            moduls.append(dif[i])

    moduls=bubble_sort(moduls)

    untypical=[0,0]

    T=0
    for d in dif:
        if d>=0:
            untypical[0]+=1
        else:
            untypical[1]+=1

    if untypical[0]>=untypical[1]:
        for i in range(len(dif)):
            if dif[i]<0:
                for k in range(len(moduls)):
                    if moduls[k] == -1*dif[i]:
                        T+=k+1
    else:
        for i in range(len(dif)):
            if dif[i]>0:
                for k in range(len(moduls)):
                    if moduls[k] == 1*dif[i]:
                        T+=k+1

    Tcrit=3 # for 7 patients should change for table
    result=[T, dif]
    return result

# Preparing files
mypath='D:\Epoc+\Tetervak2205'
filelist = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
for i in range(len(filelist)):
    filelist[i]=mypath+'\\'+filelist[i]

lf=0
for i in range(5):
    if lf<=os.path.getctime(filelist[i]):
        lf=os.path.getctime(filelist[i]) # finding the latest file

for i in range(5):
    if lf==os.path.getctime(filelist[i]):
        latest=filelist[i] # finding the latest file's name
        break

print("The latest file is: ",latest)

tovalist=[]
for i in range(len(filelist)):
    if (filelist[i][1+len(mypath)]=='t')&(filelist[i][2+len(mypath)]=='o'): # find all files which name starts with 'to' mean tova-"number of patient"_"number of test"
        tovalist.append(filelist[i])

for i in range(len(tovalist)):
    print("For the ",tovalist[i][len(mypath)+8]," test for the patient number ",tovalist[i][len(mypath)+6]," mean reaction time is: ", mean_reaction_time(xls2dict(tovalist[i])))



first=[]
second=[]
for i in range(0,len(tovalist),2):
    a=mean_reaction_time(xls2dict(tovalist[i]))
    b=mean_reaction_time(xls2dict(tovalist[i+1]))
    if (a!=-1.0) & (b!=-1.0):
        first.append(a)
        second.append(b)

good_tests=[first,second]
print("Wilcoxon rt T=",wilcoxon(good_tests)[0])

myfile = open("rtdif.txt", "w")
for i in wilcoxon(good_tests)[1]:
         myfile.write(str(i) + '\n')



first=[]
second=[]
for i in range(0,len(tovalist),2):
    a=missed(xls2dict(tovalist[i]))
    b=missed(xls2dict(tovalist[i+1]))
    if (a!=-1.0) & (b!=-1.0):
        first.append(a)
        second.append(b)

good_tests=[first,second]
print("Wilcoxon missed T=",wilcoxon(good_tests)[0])

myfile = open("misseddif.txt", "w")
for i in wilcoxon(good_tests)[1]:
         myfile.write(str(i) + '\n')


first=[]
second=[]
for i in range(0,len(tovalist),2):
    a=mistakes(xls2dict(tovalist[i]))
    b=mistakes(xls2dict(tovalist[i+1]))
    if (a!=-1.0) & (b!=-1.0):
        first.append(a)
        second.append(b)

good_tests=[first,second]

print("Wilcoxon mistakesdif T=",wilcoxon(good_tests)[0])

myfile = open("mistakesdif.txt", "w")
for i in wilcoxon(good_tests)[1]:
         myfile.write(str(i) + '\n')


first=[]
second=[]
for i in range(0,len(tovalist),2):
    a=correct(xls2dict(tovalist[i]))
    b=correct(xls2dict(tovalist[i+1]))
    if (a!=-1.0) & (b!=-1.0):
        first.append(a)
        second.append(b)

good_tests=[first,second]
print("Wilcoxon correctdif T=",wilcoxon(good_tests)[0])

myfile = open("correctdif.txt", "w")
for i in wilcoxon(good_tests)[1]:
         myfile.write(str(i) + '\n')




'''
bootstraprt=[]
path='C:'+'\\'+'Unbelivable Important Folder\mrt.dat'
with open(path) as datfile:
    data=datfile.read().splitlines()
zero=[]
for value in data:
    bootstraprt.append(float(value))
    zero.append(0)
good_tests=[bootstraprt,zero]
print("Wilcoxon mrt T=",wilcoxon(good_tests)[0])


bootstrapcorr=[]
path='C:'+'\\'+'Unbelivable Important Folder\mcorrect.dat'
zero=[]
with open(path) as datfile:
    data=datfile.read().splitlines()

for value in data:
    zero.append(0)
    bootstrapcorr.append(float(value))
good_tests=[bootstrapcorr,zero]
print("Wilcoxon mcorr T=",wilcoxon(good_tests)[0])


bootstrapmmissed=[]
zero=[]
path='C:'+'\\'+'Unbelivable Important Folder\mmissed.dat'
with open(path) as datfile:
    data=datfile.read().splitlines()

for value in data:
    zero.append(0)
    bootstrapmmissed.append(float(value))
good_tests = [bootstrapmmissed, zero]
print("Wilcoxon mmisses T=", wilcoxon(good_tests)[0])


bootstrapmistakes=[]
zero=[]
path='C:'+'\\'+'Unbelivable Important Folder\mmistakes.dat'
with open(path) as datfile:
    data=datfile.read().splitlines()

for value in data:
    zero.append(0)
    bootstrapmistakes.append(float(value))
good_tests = [bootstrapmistakes, zero]
print("Wilcoxon mmistakes T=", wilcoxon(good_tests)[0])
'''