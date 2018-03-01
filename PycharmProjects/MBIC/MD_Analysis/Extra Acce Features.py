from tkinter import Tk
from tkinter.filedialog import askopenfilename
import statistics
from scipy.signal import butter, lfilter
from numpy import fft
from math import sqrt
from copy import deepcopy
import matplotlib.pyplot as plt


stages=['Background', 'First TOVA test', 'Hyperventilation', 'Second TOVA test', 'Aftereffect']

featuresNames=['Max','Min','Mean','STD','ZCR','Energy']

def Motion_Data_2_Dict(Path2MotionFile):
    notanumber=True
    label=''
    value=[]
    with open(Path2MotionFile) as file:
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
                value.append(line)
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

def axis_feature(axis):
    features=[max(axis),min(axis),statistics.mean(axis),statistics.stdev(axis)]
    zcr=0
    for i in range(len(axis)):
        if((axis[i]>0) and (axis[i-1]<0))or((axis[i]<0) and (axis[i-1]>0)):
            zcr+=1

    features.append(zcr)
    AXIS=fft.fft(axis)
    energy=0
    for i in range(len(AXIS)):
        energy +=abs(AXIS[i])**2
    energy/=len(AXIS)
    features.append(energy)
    return {featuresNames[i]:features[i] for i in range(len(features))}

def activity(x,y,z,rate=1.1): # Take three axis arrays, return activity and (Peak time) / (Peak number)
    arr=[]
    for i in range(1,len(x),1):
        arr.append(sqrt((x[i]-x[i-1])**2+(y[i]-y[i-1])**2+(z[i]-z[i-1])**2))
    level=statistics.median(arr)*rate
    peakTime=0
    peakCount=0
    for i in range(len(arr)):
        if(arr[i]>0):
            if(arr[i]>level):
                peakTime+=1
                if(arr[i-1]<=level):
                    peakCount+=1
        else:
            if(arr[i]<level):
                peakTime+=1
                if(arr[i-1]>=level):
                    peakCount+=1



    plt.plot(arr)
    plt.axis([10,len(arr),0,0.25])
    plt.show()
    return sum(arr), peakTime/peakCount

def avZCR(x,y,z):
    return (x['ZCR']+y['ZCR']+z['ZCR'])/3

def avEn(x,y,z):
    return (x['Energy']+y['Energy']+z['Energy'])/3

def get_patient_name(path):
    slash=0
    reverse_name=''
    for i in range(len(path)-1,-1,-1):
        if (path[i]=='/' or path[i]=='\\' ):
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

try:
    #path2File='C:/Users/Dante/Desktop/EpocData/05.06_Сысков/Patient_MotionData.csv'
    mdDict = Motion_Data_2_Dict(path2File)
except:
    Tk().withdraw()
    path2File = askopenfilename(filetypes =(("CSV File", "*.csv"),("Text File", "*.txt"), ("All Files","*.*")),
                               title = "Choose motion data"
                               )
    if(path2File==''):
        exit(0)
    mdDict=Motion_Data_2_Dict(path2File)

fs = int(len(mdDict['TIMESTAMP']) / (mdDict['TIMESTAMP'][-1] - mdDict['TIMESTAMP'][0]))
g = round(statistics.mean(mdDict['ACCX'])-statistics.mean(butter_bandpass_filter(mdDict['ACCX'],0.3,20,fs)),3)
startTime=mdDict['TIMESTAMP'][0]
for i in range(len(mdDict['TIMESTAMP'])):
    mdDict['TIMESTAMP'][i]-=startTime


'''''''''''''''
 Time stages
 
times=[300598,498480,679465,877370] # Syskov only
for t in range(len(times)):
    times[t]/=1000
 
'''''''''''''''
times = [5, 8.3, 11.3, 14.6]
for i in range(len(times)):
    times[i] *= 60

timeStages=[0]
i=0
for k in range(len(mdDict['TIMESTAMP'])):
    if(mdDict['TIMESTAMP'][k]>times[i]):
        timeStages.append(k)
        i+=1
        if(i==len(times)):
            break
timeStages.append(len(mdDict['TIMESTAMP']))

'''''''''''''''
 Preparing axis
'''''''''''''''
Axis=['ACCX','ACCY','ACCZ']
for i in range(len(Axis)):
    mdDict[Axis[i]]=butter_bandpass_filter(mdDict[Axis[i]],0.3,20,fs)
    for k in range(len(mdDict[Axis[i]])):
        mdDict[Axis[i]][k]/=g
    mdDict[Axis[i]]={stages[z]:mdDict[Axis[i]][timeStages[z]:timeStages[z+1]] for z in range(len(timeStages)-1)}

featureDict={Axis[k]:{stages[i]:axis_feature(mdDict[Axis[k]][stages[i]]) for i in range(len(stages))} for k in range(len(Axis))}

nonAxisp=['Average ZCR', 'Average Energy', 'Activity Index', 'Average activity time']
columnNames=deepcopy(nonAxisp)
nonAxis={stages[i]:{nonAxisp[k]:0 for k in range(len(nonAxisp))} for i in range(len(stages))}

axStDict = []
for i in range(len(stages)):
    nonAxis[stages[i]]['Average ZCR']= avZCR(featureDict["ACCX"][stages[i]],featureDict["ACCY"][stages[i]],featureDict["ACCZ"][stages[i]])
    nonAxis[stages[i]]['Average Energy']=avEn(featureDict["ACCX"][stages[i]],featureDict["ACCY"][stages[i]],featureDict["ACCZ"][stages[i]])
    nonAxis[stages[i]]['Activity Index']=activity(mdDict["ACCX"][stages[i]],mdDict["ACCY"][stages[i]],mdDict["ACCZ"][stages[i]])[0]
    nonAxis[stages[i]]['Average activity time']=activity(mdDict["ACCX"][stages[i]],mdDict["ACCY"][stages[i]],mdDict["ACCZ"][stages[i]])[1]


for k in range(len(Axis)):
    for i in range(len(featuresNames)):
        axStDict.append(Axis[k]+'_'+featuresNames[i])

for i in range (len(axStDict)):
    columnNames.append(axStDict[i])

axStDict={stages[z]:{axStDict[i]:featureDict[axStDict[i][:4]][stages[z]][axStDict[i][5:]] for i in range(len(axStDict))} for z in range(len(stages))}


'''''''''''''''''
 All features dictionary
'''''''''''''''''
finalDict=nonAxis
for i in range(len(stages)):
    finalDict[stages[i]].update(axStDict[stages[i]])


'''''''''''''''''
 writing to Clusters csv
'''''''''''''''''
from os import makedirs
from os.path import exists

path2ClustersACCE='C:\Clusters\Acce'
if not exists(path2ClustersACCE):
    makedirs(path2ClustersACCE)

clusterFileExist=False
try:
    open(path2ClustersACCE+'\Acce features.csv','r')
    clusterFileExist=True
except:
    clusterFileExist = False


with open(path2ClustersACCE+'\Acce features.csv', 'a') as file:
    if not clusterFileExist:
        line='Subject;'
        for k in range(len(columnNames)):
            line+=columnNames[k]+';'
        line=line[:len(line)-1] # all without last ';'
        line+='\n'
        file.write(line)

    patientName=get_patient_name(path2File)

    for i in range(len(stages)):
        line = patientName+'_'+stages[i]+';'
        for k in range(len(columnNames)):
            line+=str(finalDict[stages[i]][columnNames[k]])+';'
        line=line[:len(line)-1] # all without last ;
        line+='\n'
        file.write(line)
    file.close()


