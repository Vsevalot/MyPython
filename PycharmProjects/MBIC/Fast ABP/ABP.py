channels = ['IED_AF3', 'IED_F7', 'IED_F3', 'IED_FC5', 'IED_T7', 'IED_P7', 'IED_O1', 'IED_O2', 'IED_P8',
            'IED_T8', 'IED_FC6', 'IED_F4', 'IED_F8', 'IED_AF4']
rhythms = ['Theta', 'Alpha', 'BetaL', 'BetaH']

stages = ['Background', 'First TOVA test', 'Hyperventilation', 'Second TOVA test', 'Aftereffect']

def ABP_data2Dict(Path2ABPFile):
    notanumber=True
    label=''
    value=[]
    with open(Path2ABPFile) as file:
        while(notanumber): # read until find numbers, previous line - label
            line = file.readline()
            if((line=='\n') or (line=='')):
                continue
            line=line.split(';')
            while((line[-1] == '\n') or ((line[-1] == ''))):
                newitem=''
                for i in range(len(line[-1])-1):
                    newitem+=line[-1][i]
                del line[-1]
                if(len(newitem)):
                    line.append(newitem)
            try:
                for i in range(len(line)):
                    line[i] = float(line[i])
                #value.append(line) usually first line is broken and contains 0
                notanumber=False
            except(ValueError):
                label=line
                for i in range(len(label)):
                    newitem = ''
                    for letter in label[i]:
                        if letter==' ':
                            continue
                        newitem+=letter
                    label[i]=newitem

        for i in range(10):
            line = file.readline() # very noisy lines

        while(len(line)):
            line = file.readline()
            if((line=='\n') or (line=='')):
                continue
            line=line.split(';')
            while ((line[-1][-1] == '\n') or ((line[-1] == '')) or (line[-1]=='\n')):
                newitem = ''
                for i in range(len(line[-1]) - 1):
                    newitem += line[-1][i]
                del line[-1]
                if (len(newitem)):
                    line.append(newitem)
            for i in range(len(line)):
                line[i]=float(line[i])
            value.append(line)

        k=-1

        cvalue=[]
        for i in range(len(value[0])):
            column=[]
            for k in range(len(value)):
                column.append(value[k][i])
            cvalue.append(column)

    arr=[]
    for i in range(1,len(cvalue),5):
        arr.append({rhythms[k]:cvalue[i+k] for k in range(len(rhythms))})

    if(len(channels)==len(arr)):
        valuedict={channels[i]:arr[i] for i in range(len(channels))}
    valuedict['TIMESTAMP']=cvalue[0]

    return valuedict

def index(channel):
    stagesNames = ['Background', 'First TOVA test', 'Hyperventilation', 'Second TOVA test', 'Aftereffect']
    allpower={stage:0 for stage in stagesNames}
    for rhythm in channel:
        for stage in channel[rhythm]:
            allpower[stage]+=channel[rhythm][stage]

    for rhythm in channel:
        for stage in channel[rhythm]:
            channel[rhythm][stage]=round(channel[rhythm][stage]/allpower[stage],2)
    return channel

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

from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()
path2File = askopenfilename(initialdir="C:\\Users\Dante\Desktop\EpocData",
                           filetypes =(("CSV File", "*.csv"),("Text File", "*.txt"), ("All Files","*.*")),
                           title = "Choose an EEG data file"
                           )
if(path2File==''):
    exit(0)
my=ABP_data2Dict(path2File)

startTime=my['TIMESTAMP'][0]
timedel=1
if(my['TIMESTAMP'][0]>20000):
    timedel=1000
for i in range(len(my['TIMESTAMP'])):
    my['TIMESTAMP'][i]=(my['TIMESTAMP'][i]-startTime)/timedel


stamps = [5, 8.2, 11.4, 14.6, 19.6]
for i in range(len(stamps)):
    stamps[i] *= 60

if (stamps[-1]>my['TIMESTAMP'][-1]):
    stamps[-1] = my['TIMESTAMP'][-2]

stageTime = [0]
k = 0
for i in range(len(my['TIMESTAMP'])):
    if (my['TIMESTAMP'][i] > stamps[k]):
        stageTime.append(i)
        k += 1
        if (k == len(stamps)):
            break


for i in range(len(channels)):
    for k in range(len(rhythms)):
        my[channels[i]][rhythms[k]]={stages[z]:my[channels[i]][rhythms[k]][stageTime[z]:stageTime[z+1]] for z in range(len(stages))}


for i in range(len(channels)):
    for k in range(len(rhythms)):
        for z in range(len(stages)):
            my[channels[i]][rhythms[k]][stages[z]]=sum(my[channels[i]][rhythms[k]][stages[z]])
            print(channels[i],rhythms[k],stages[z],my[channels[i]][rhythms[k]][stages[z]])

eegDict=my

fullCSV=[]
for i in range(len(stages)):
    fullCSV.append([''])
    for k in range(len(channels)):
        eegDict[channels[k]]=index(eegDict[channels[k]])
        fullCSV[i].append(channels[k]+';')

'''''''''''''''''
# preparing to csv
'''''''''''''''''
for i in range(len(stages)):
    fullCSV[i][0] += str(stages[i])
    fullCSV[i][0] += ';'
    for rhythm in rhythms:
        fullCSV[i][0]+=rhythm
        fullCSV[i][0]+=';'

for i in range(len(stages)):
    for k in range(len(channels)):
        for rhythm in rhythms:
            fullCSV[i][k+1]+=str(eegDict[channels[k]][rhythm][stages[i]])
            fullCSV[i][k+1]+=';'


'''''''''''''''''
# writing to csv
'''''''''''''''''
csvName=get_patient_name(path2File)
path2Save=get_folder(path2File)
path2Save+='/Analysed'

from os import makedirs
from os.path import exists
if not exists(path2Save):
    makedirs(path2Save)

for i in range(len(stages)):
    with open(path2Save+'/'+csvName +' '+ stages[i]+'.csv', 'w') as file:
        for line in fullCSV[i]:
            file.write(line)
            file.write('\n')
        file.close()

'''''''''''''''''
# writing to ANOVA csv
'''''''''''''''''
path2ANOVAEEG='C:\ANOVA\EEG\ABP'

if not exists(path2ANOVAEEG):
    makedirs(path2ANOVAEEG)

for i in range(len(channels)):
    for k in range(len(rhythms)):
        try:
            with open(path2ANOVAEEG+'\\'+channels[i]+'_'+rhythms[k]+'.csv', 'a') as file:
                l=''
                for z in range(len(stages)):
                    l+=str(eegDict[channels[i]][rhythms[k]][stages[z]])+';'
                line=l[:len(l)-1] # all without last ;
                line+='\n'
                file.write(line)
                file.close()
        except:
            with open(path2ANOVAEEG+'\\'+channels[i]+'_'+rhythms[k]+'.csv', 'w') as file:
                l=''
                for z in range(len(stages)):
                    l+=str(eegDict[channels[i]][rhythms[k]][stages[z]])+';'
                line=l[:len(l)-1] # all without last ;
                line+='\n'
                file.write(line)
                file.close()

print(csvName)