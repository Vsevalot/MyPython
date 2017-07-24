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

path2csv='C:\ANOVA\TOVA'
csvFiles = [join(path2csv, f) for f in listdir(path2csv) if isfile(join(path2csv, f))]

tests=[]
for file in csvFiles:
    with open(file,'r') as csv:
        l=csv.read().split('\n')
        if(l[-1]==''):
            del l[-1]
        for i in range(len(l)):
            l[i]=l[i].split(';')
        l=transponate(l)
    tests.append(l)

for i in range(len(tests[0])):
    test = stats.wilcoxon(tests[0][i],tests[1][i]).pvalue
    print(test)











