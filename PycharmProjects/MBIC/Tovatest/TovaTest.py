from numpy import std

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
        return round(M / n,3)

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

def std_for_time(dictionary):
    times=[]
    for i in range(len(dictionary['rt'])):
        if ((dictionary['rt'][i]>0)&(dictionary['corr'][i]==1)):
            times.append(dictionary['rt'][i])
    return round(std(times),3)

def moda(arr):
    if len(arr)%2==1:
        return arr[(len(arr)-1)/2]
    else:
        return arr[(len(arr))/2] + arr[len(arr)/2 - 1]

def get_patient_name(path):
    slash=0
    reverse_name=''
    for i in range(len(path)-1,-1,-1):
        if (path[i]=='/'):
            slash+=1
            continue
        if (slash == 1):
            reverse_name+=path[i]
        if (slash == 2):
            break
    name=''
    for i in range(len(reverse_name) - 1, -1, -1):
        name+=reverse_name[i]
    return name

def find_first_test(arr):
    if((arr[0][-5]=='1')&(arr[1][-5]=='2')):
        return [0,1]
    elif((arr[1][-5]=='1')&(arr[0][-5]=='2')):
        return [1,0]
    else:
        print('Can not determinate first and second tests. Check names of files. The name should be like "toav-NumberOfResearch_1.xls", "toav-NumberOfResearch_2.xls"')
        exit(33)

def get_folder(path):
    slash = 0
    for i in range(len(path) - 1, -1, -1):
        if (path[i] == '/'):
            slash+=1

    path2folder=''
    for i in range(len(path)):
        if (path[i] == '/'):
            slash-=1
        if (slash==0):
            break
        path2folder+=path[i]

    return path2folder


    name = ''
    for i in range(len(reverse_name) - 1, -1, -1):
        name += reverse_name[i]
    return name

'''''''''''''''
# Preparing files
'''''''''''''''
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

Tk().withdraw()
paths2Files = askopenfilenames(initialdir="C:\\Users\Dante\Desktop\EpocData",
                           filetypes =(("XLS File", "*.xls"),("CSV File", "*.csv"),("Text File", "*.txt"), ("All Files","*.*")),
                           title = "Choose two patient's TOVA test files"
                           )


patienName=get_patient_name(paths2Files[0])

tovaList=[xls2dict(paths2Files[find_first_test(paths2Files)[0]]),xls2dict(paths2Files[find_first_test(paths2Files)[1]])] # list of 2 tests in correct order

functionList=[correct,missed,mistakes,mean_reaction_time,std_for_time] # all functions we need to apply
parameterNames=['Number of correct reactions','Number of missed stimulus','Number of false reactions','Mean reaction time','STD of reaction time' ] # Names for results of the functions


forCSV=[patienName+';First test;Second test\n']
for i in range(len(functionList)):
    line=''
    line+=parameterNames[i]
    line+=';'
    line+=str(functionList[i](tovaList[0]))
    line+=';'
    line+=str(functionList[i](tovaList[1]))
    line+='\n'
    forCSV.append(line)

path2Save=get_folder(paths2Files[0])
path2Save+='/Analysed'

from os import makedirs
from os.path import exists
if not exists(path2Save):
    makedirs(path2Save)

with open(path2Save+'/'+patienName+' results of TOVA.csv','w') as file:
    for line in forCSV:
        file.write(line)
    file.close()

'''''''''''''''''
# writing to ANOVA csv
'''''''''''''''''

path2ANOVA='C:\ANOVA'

if not exists(path2ANOVA):
    makedirs(path2ANOVA)

path2ANOVATOVA='C:\ANOVA\TOVA'

if not exists(path2ANOVATOVA):
    makedirs(path2ANOVATOVA)

'''''''''''''''''
# First test
'''''''''''''''''
try:
    with open(path2ANOVATOVA+'\\FirstTest.csv','a') as csv:
        l=''
        for i in range(len(functionList)):
            l += str(functionList[i](tovaList[0])) + ';'
        line=l[:len(l)-1]
        line+='\n'
        csv.write(line)
except:
    with open(path2ANOVATOVA+'\\FirstTest.csv','w') as csv:
        l=''
        for i in range(len(functionList)):
            l += str(functionList[i](tovaList[0])) + ';'
        line=l[:len(l)-1]
        line+='\n'
        csv.write(line)


'''''''''''''''''
# Second test
'''''''''''''''''
try:
    with open(path2ANOVATOVA+'\\SecondTest.csv','a') as csv:
        l=''
        for i in range(len(functionList)):
            l += str(functionList[i](tovaList[1])) + ';'
        line=l[:len(l)-1]
        line+='\n'
        csv.write(line)
except:
    with open(path2ANOVATOVA+'\\SecondTest.csv','w') as csv:
        l=''
        for i in range(len(functionList)):
            l += str(functionList[i](tovaList[1])) + ';'
        line=l[:len(l)-1]
        line+='\n'
        csv.write(line)

print(patienName)