from os import listdir
from os.path import isfile, join
from scipy import stats

def transponate(arr):
    all=[]
    for i in range(len(arr[0])):
        column = []
        for k in range(len(arr)):
            column.append(float(arr[k][i]))
        all.append(column)
    return all

path2csv='C:\ANOVA\EEG'
csvFiles = [join(path2csv, f) for f in listdir(path2csv) if isfile(join(path2csv, f))]

for file in csvFiles:
    with open(file,'r') as csv:
        l=csv.read().split('\n')
        if(l[-1]==''):
            del l[-1]
        for i in range(len(l)):
            l[i]=l[i].split(';')
        l=transponate(l)
        test=stats.kruskal(l[0],l[1],l[2],l[3],l[4]).pvalue
        if(test<0.05):
            print(test)














