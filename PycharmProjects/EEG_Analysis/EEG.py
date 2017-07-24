import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from math import sqrt
from numpy import array, mean, std, fft

def EEGData2Dict(Path2EEGEFile):
    notanumber=True
    label=''
    value=[]
    with open(Path2EEGEFile) as file:
        while(notanumber): # read until find numbers, previous line - label
            line = file.readline()
            if((line=='\n') or (line=='')):
                continue
            line=line.split(';')
            while((line[-1][-1] == '\n') or ((line[-1] == ''))):
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

        cvalue=[]
        for i in range(len(value[0])):
            column=[]
            for k in range(len(value)):
                column.append(value[k][i])
            cvalue.append(column)

        if(len(label)==len(cvalue)):
            valuedict = {label[i]:cvalue[i] for i in range(len(label))}
            return valuedict
        else:
            print("Something goes wrong, check number of labels and number of data columns")
            exit(33)

def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

def three_sigma_cleaning(eegD,chan):
    m=mean(eegD[chan])
    s=std(eegD[chan])
    hborder=m+3*s
    lborder=m-3*s
    for i in range(len(eegD[chan])):
        if ((eegD[chan][i]>hborder) or (eegD[chan][i]<lborder) and (i!=len(eegD[chan])-1)):
            for key in eegD:
                del eegD[key][i]

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
my=EEGData2Dict(path2File)
channels=['IED_AF3','IED_F7','IED_F3','IED_FC5','IED_T7','IED_P7','IED_O1','IED_O2','IED_P8','IED_T8','IED_FC6','IED_F4','IED_F8','IED_AF4']
rhythms=['Theta','Alpha','BetaL','BetaH']
dictList=[]
for i in range(len(channels)):
    dictList.append({rhythms[i]:1 for i in range(len(rhythms))})

eegDict={channels[i]:dictList[i] for i in range(len(channels))}

fs=int(len(my['IED_TIMESTAMP']) / (my['IED_TIMESTAMP'][-1] - my['IED_TIMESTAMP'][0]))

diapasons=[4,7,7,15,15,25,25,31] # diapason for rhythms

'''''''''''''''''
# convert to voltage
'''''''''''''''''
level=4180
voltage=0.51
for i in range(len(channels)):
    for k in range(len(my[channels[i]])):
        my[channels[i]][k]-=level
        my[channels[i]][k] *= voltage
        my[channels[i]][k] = round(my[channels[i]][k],2)


for key in eegDict:
    for i in range(len(eegDict[key])):
        eegDict[key][rhythms[i]]=butter_bandpass_filter(my[key],diapasons[i*2],diapasons[i*2+1],fs)



stamps = [5, 8.2, 11.4, 14.6, 19.6]
for i in range(len(stamps)):
    stamps[i] *= 60
    stamps[i] += my['IED_TIMESTAMP'][0]

if (stamps[-1]>my['IED_TIMESTAMP'][-1]):
    stamps[-1] = my['IED_TIMESTAMP'][-2]

stageTime = [0]
k = 0
for i in range(len(my['IED_TIMESTAMP'])):
    if (my['IED_TIMESTAMP'][i] > stamps[k]):
        stageTime.append(i)
        k += 1
        if (k == len(stamps)):
            break

stagesNames = ['Background', 'First TOVA test', 'Hyperventilation', 'Second TOVA test', 'Aftereffect']

for key in eegDict:
    for rhythm in eegDict[key]:
        eegDict[key][rhythm]={stagesNames[i]:eegDict[key][rhythm][stageTime[i]:stageTime[i+1]] for i in range(len(stagesNames))}


i=0
for key in eegDict:
    for rhythm in eegDict[key]:
        for stage in eegDict[key][rhythm]:
            eegDict[key][rhythm][stage]=round(sum(abs(fft.fft(eegDict[key][rhythm][stage]))),3)
            print(int(i/(len(channels)*len(rhythms)*len(stagesNames))*100),'%')
            i+=1



fullCSV=[]
for i in range(len(stagesNames)):
    fullCSV.append([''])
    for k in range(len(channels)):
        eegDict[channels[k]]=index(eegDict[channels[k]])
        fullCSV[i].append(channels[k]+';')

'''''''''''''''''
# preparing to csv
'''''''''''''''''
for i in range(len(stagesNames)):
    fullCSV[i][0] += str(stagesNames[i])
    fullCSV[i][0] += ';'
    for rhythm in rhythms:
        fullCSV[i][0]+=rhythm
        fullCSV[i][0]+=';'

for i in range(len(stagesNames)):
    for k in range(len(channels)):
        for rhythm in rhythms:
            fullCSV[i][k+1]+=str(eegDict[channels[k]][rhythm][stagesNames[i]])
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

for i in range(len(stagesNames)):
    with open(path2Save+'/'+csvName +' '+ stagesNames[i]+'.csv', 'w') as file:
        for line in fullCSV[i]:
            file.write(line)
            file.write('\n')
        file.close()

'''''''''''''''''
# writing to ANOVA csv
'''''''''''''''''
path2ANOVAEEG='C:\ANOVA\EEG\EEG'
if not exists(path2ANOVAEEG):
    makedirs(path2ANOVAEEG)

for i in range(len(channels)):
    for k in range(len(rhythms)):
        try:
            with open(path2ANOVAEEG+'\\'+channels[i]+'_'+rhythms[k]+'.csv', 'a') as file:
                l=''
                for z in range(len(stagesNames)):
                    l+=str(eegDict[channels[i]][rhythms[k]][stagesNames[z]])+';'
                line=l[:len(l)-1] # all without last ;
                line+='\n'
                file.write(line)
                file.close()
        except:
            with open(path2ANOVAEEG+'\\'+channels[i]+'_'+rhythms[k]+'.csv', 'w') as file:
                l=''
                for z in range(len(stagesNames)):
                    l+=str(eegDict[channels[i]][rhythms[k]][stagesNames[z]])+';'
                line=l[:len(l)-1] # all without last ;
                line+='\n'
                file.write(line)
                file.close()

print(csvName)


'''''''''''''''''
# writing to Clusters csv
'''''''''''''''''
path2ClustersEEG='C:\Clusters\EEG\EEG'
if not exists(path2ClustersEEG):
    makedirs(path2ClustersEEG)


with open(path2ClustersEEG+'EEG_Results.csv', 'a') as file:
    '''
    line='subject;'
    for k in range(len(channels)):
        for z in range(len(rhythms)):
            line+=str(channels[k]+'_'+rhythms[z])+';'
    line=line[:len(line)-1] # all without last ;
    line+='\n'
    file.write(line)
'''

    for i in range(len(stagesNames)):
        line = csvName+';'
        for k in range(len(channels)):
            for z in range(len(rhythms)):
                line+=str(eegDict[channels[k]][rhythms[z]][stagesNames[i]])+';'

        line=line[:len(line)-1] # all without last ;
        line+='\n'
        file.write(line)
    file.close()
