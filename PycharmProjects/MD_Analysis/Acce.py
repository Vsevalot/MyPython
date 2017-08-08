import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from math import sqrt
from numpy import array, mean, std
from matplotlib.backends.backend_pdf import PdfPages

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
path2File = askopenfilename(initialdir="C:\\Users\Dante\Desktop\Новая папка",
                           filetypes =(("CSV File", "*.csv"),("Text File", "*.txt"), ("All Files","*.*")),
                           title = "Choose a motion data file"
                           )

myDict=Motion_Data_2_Dict(path2File)

fs = int(len(myDict['TIMESTAMP']) / (myDict['TIMESTAMP'][-1] - myDict['TIMESTAMP'][0]))

x = myDict['ACCX']
y = myDict['ACCY']
z = myDict['ACCZ']
row = [x, y, z]
rNames = ['Row acce X data', 'Row acce Y data', 'Row acce Z data']
X = butter_bandpass_filter(myDict['ACCX'], 0.3, 20, fs)
Y = butter_bandpass_filter(myDict['ACCY'], 0.3, 20, fs)
Z = butter_bandpass_filter(myDict['ACCZ'], 0.3, 20, fs)
filtered = [X, Y, Z]
fNames = ['Filtered acce X data', 'Filtered acce Y data', 'Filtered acce Z data']

stamps = [5, 8.2, 11.4, 14.6,19.6]
for i in range(len(stamps)):
    stamps[i] *= 60
    stamps[i] += myDict['TIMESTAMP'][0]

stageTime = [0]
k = 0
for i in range(len(myDict['TIMESTAMP'])):
    if (myDict['TIMESTAMP'][i] > stamps[k]):
        stageTime.append(i)
        k += 1
        if (k == len(stamps)):
            break

acceModule = []
for i in range(len(X)):
    acceModule.append(sqrt(X[i] * X[i] + Y[i] * Y[i] + Z[i] * Z[i]))

g = 0
for i in range(len(acceModule)):
    g += acceModule[i]
g /= len(acceModule)
g *= 7

for i in range(len(acceModule)):
    acceModule[i] /= g

stages = []
for i in range(len(stamps)):
    stages.append(array(acceModule[stageTime[i]:stageTime[i + 1]]))
    print(stageTime[i + 1],'/',len(acceModule))

stagesNames = ['Background', 'First TOVA test', 'Hyperventilation', 'Second TOVA test', 'Aftereffect']
stagesDict = {stagesNames[i]: stages[i] for i in range(len(stages))}

meanValue = []
stdValue = []
for key in stagesDict:
    meanValue.append(mean(stagesDict[key]))
    stdValue.append(std(stagesDict[key]))

forCSV = [';Mean;STD\n']
for i in range(len(stagesNames)):
    forCSV.append(stagesNames[i] + ';')

for i in range(len(meanValue)):
    forCSV[i + 1] += str(round(meanValue[i],3))
    forCSV[i + 1] += ';'
    forCSV[i + 1] += str(round(stdValue[i],3))
    forCSV[i + 1] += '\n'



csvName=get_patient_name(path2File)
path2Save=get_folder(path2File)
path2Save+='/Analysed'

from os import makedirs
from os.path import exists
if not exists(path2Save):
    makedirs(path2Save)



with open(path2Save+'/'+csvName+" Accelerometer" +'.csv', 'w') as file:
    for line in forCSV:
        file.write(line)
    file.close()


pd=PdfPages('test.pdf')
plt.figure(figsize=(24.0, 15.0))
plt.rc('font', size=26)
for i in range(6):

    if (i < 3):
        plt.subplot(2, 3, i + 1)
        plt.plot(myDict['TIMESTAMP'], row[i])
        plt.title(rNames[i])
        plt.xlabel('Time(sec)')
        plt.ylabel('Value')
    else:
        plt.subplot(2, 3, i + 1)
        plt.plot(myDict['TIMESTAMP'], filtered[i - 3])
        plt.title(fNames[i - 3])
        plt.xlabel('Time(sec)')
        plt.ylabel('Value')
pd.savefig()

plt.figure(figsize=(24.0, 15.0))
plt.plot(myDict['TIMESTAMP'], acceModule)
plt.title("Accelerometer's value module at different stages")
plt.axis([myDict['TIMESTAMP'][0] + 20, myDict['TIMESTAMP'][stageTime[-1]], 0, 4])
for i in range(1, len(stageTime), 1):
    plt.plot((myDict['TIMESTAMP'][stageTime[i]], myDict['TIMESTAMP'][stageTime[i]]), (0, 4), 'r--')
plt.xlabel('Time(sec)')
plt.ylabel('Value(g)')
for i in range(len(stagesNames)):
    plt.text(myDict['TIMESTAMP'][stageTime[i]] + 50, 3.5, stagesNames[i],
             bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
pd.savefig()
pd.close()


'''''''''''''''''
# writing to ANOVA csv
'''''''''''''''''
path2ANOVA='C:\ANOVA\MD\Acce'
if not exists(path2ANOVA):
    makedirs(path2ANOVA)


try: # Mean value
    with open(path2ANOVA+'\Mean.csv','a') as file:
        line=''
        for i in range(len(meanValue)):
            line+=str(meanValue[i])+';'
        line=line[:len(line)-1]
        line+='\n'
        file.write(line)
        file.close()
except:
    with open(path2ANOVA+'\Mean.csv','w') as file:
        line=''
        for i in range(len(meanValue)):
            line+=str(meanValue[i])+';'
        line=line[:len(line)-1]
        line+='\n'
        file.write(line)
        file.close()

try: # STD value
    with open(path2ANOVA+'\STD.csv','a') as file:
        line=''
        for i in range(len(stdValue)):
            line+=str(stdValue[i])+';'
        line=line[:len(line)-1]
        line+='\n'
        file.write(line)
        file.close()
except:
    with open(path2ANOVA+'\STD.csv','w') as file:
        line=''
        for i in range(len(stdValue)):
            line+=str(stdValue[i])+';'
        line=line[:len(line)-1]
        line+='\n'
        file.write(line)
        file.close()

print(csvName)