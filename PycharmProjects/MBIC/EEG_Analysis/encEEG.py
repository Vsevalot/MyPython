channels=['f3f1','f4a2','c3a1','c4a2','p3a1','p4a2','o1a1','o2a2','a1a2']
rhythms=['Theta','Alpha','BetaL','BetaH']
stages= ['Background', 'First TOVA test', 'Hyperventilation', 'Second TOVA test', 'Aftereffect']

def readCSV(path2csv:str) -> list: # read any CSV file and return it like list of columns
    with open(path2csv, 'r') as file:
        lines=[line.split(';') for line in file.readlines()] # reading all lines in the file with rows as elements of the list
        emptyLine=True
        while(emptyLine): # remove all empty lines
            for value in lines[-1]:
                if(value!='' or value!='\n'):
                    emptyLine=False
            if(emptyLine):
                del lines[-1]

        squareCSV=True
        for line in range(len(lines)): # check for square form of the csv (the number of columns is constant in the file)
            if(lines[line][-1][-1]=='\n'): # remove '\n' symbol which ends a line
                lines[line][-1]=lines[line][-1][:-1]
            if(len(lines[line])!=len(lines[0])):
                squareCSV=False
                print("CSV file: "+path2csv+" does not have square form (the number of columns is changing through the file)")
                exit(1)
        if(squareCSV):
            data=[[value[i] for value in lines] for i in range(len(lines[0]))] # transpose the list to make columns elements of the list
            return data

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

def global_index(dict):
    globalPower=0
    for z in range(len(stagesNames)):
        for i in range(len(channels)):
            for k in range(len(rhythms)):
                globalPower+=dict[channels[i]][rhythms[k]][stagesNames[z]]
    for i in range(len(channels)):
        for k in range(len(rhythms)):
            for z in range(len(stagesNames)):
                dict[channels[i]][rhythms[k]][stagesNames[z]]=round(10*dict[channels[i]][rhythms[k]][stagesNames[z]]/globalPower,6)
    return dict

filePath="E:\\test\somestaff\csv\\Vasilyev.csv"

data=readCSV(filePath)[:-3]

eegDict={'IED_TIMESTAMP':data[0]}
for i in range(len(eegDict['IED_TIMESTAMP'])):
    eegDict['IED_TIMESTAMP'][i]=float(eegDict['IED_TIMESTAMP'][i])/1000

for channel in range(len(channels)):
    for i in range(len(data[channel+1])):
        data[channel + 1][i]=float(data[channel+1][i])
        eegDict[channels[channel]]={'1':1}


diapasons=[4,7,7,15,15,25,25,31] # diapason for rhythms


for channel in range(len(channels)):
    for i in range(len(rhythms)):
        eegDict[channels[channel]][rhythms[i]]=butter_bandpass_filter(data[channel+1],diapasons[i*2],diapasons[i*2+1],250)
        eegDict[channels[channel]].pop('1',None)

print(eegDict["IED_TIMESTAMP"][-1])
stamps = [5, 8.2, 11.4, 14.6, 19.6]
for i in range(len(stamps)):
    stamps[i] *= 60
    stamps[i] += eegDict['IED_TIMESTAMP'][0]

if (stamps[-1]>eegDict['IED_TIMESTAMP'][-1]):
    stamps[-1] = eegDict['IED_TIMESTAMP'][-2]

stageTime = [0]
k = 0
for i in range(len(eegDict['IED_TIMESTAMP'])):
    if (eegDict['IED_TIMESTAMP'][i] > stamps[k]):
        stageTime.append(i)
        k += 1
        if (k == len(stamps)):
            break

stagesNames = ['Background', 'First TOVA test', 'Hyperventilation', 'Second TOVA test', 'Aftereffect']

for channel in channels:
    for rhythm in eegDict[channel]:
        eegDict[channel][rhythm]={stagesNames[i]:eegDict[channel][rhythm][stageTime[i]:stageTime[i+1]] for i in range(len(stagesNames))}


i=0
for key in channels:
    for rhythm in eegDict[key]:
        for stage in eegDict[key][rhythm]:
            eegDict[key][rhythm][stage]=round(sum([x**2 for x in abs(fft.fft(eegDict[key][rhythm][stage]))]),3)
            print(int(i/(len(channels)*len(rhythms)*len(stagesNames))*100),'%')
            i+=1

eegDict=global_index(eegDict)

final=[]
for stage in range(len(stagesNames)):
    a = 0
    b = 0
    t = 0
    for channel in channels:
        a+=eegDict[channel]['Alpha'][stagesNames[stage]]
        b+=eegDict[channel]['BetaH'][stagesNames[stage]]
        t+=eegDict[channel]['Theta'][stagesNames[stage]]
    final.append([a/t,b/t])


with open("E:\\test\\AlphaThetaEnc.csv",'a')as file:
    line=''
    for stage in range(len(stagesNames)):
        for i in range(len(final[stage])):
            line+=str(round(final[stage][i],3))+';'
    line=line[:-1]
    line+='\n'
    file.write(line)