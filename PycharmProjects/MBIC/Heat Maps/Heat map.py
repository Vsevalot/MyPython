import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import scipy.ndimage as sp
from copy import deepcopy

stages=['Background', 'First TOVA test', 'Hyperventilation', 'Second TOVA test', 'Aftereffect']
rhythms=['Theta','Alpha','BetaL','BetaH']
channels=['IED_AF3','IED_F7','IED_F3','IED_FC5','IED_T7','IED_P7','IED_O1','IED_O2','IED_P8','IED_T8','IED_FC6','IED_F4','IED_F8','IED_AF4']
for i in range(len(channels)): # del IED_
    channels[i]=channels[i][4:]

def indexes_reader(path2indexes):
    stage=[0]*14*4
    mean=[]
    for i in range(5):
        mean.append(stage.copy())
    title=[]
    z=-1
    with open(path2indexes) as file:
        for line in file:
            z+=1
            try:
                float(line.split(';')[1])
                numbers=line.split(';')[1:]
                for i in range(len(mean[0])):
                    mean[z%5][i]+=float(numbers[i])
            except:
                title=line.split(';')[1:]
                if(title[-1][-1]=='\n'):
                    title[-1]=title[-1][:-1] # remove '\n' from last element
                if(title[0][0]=='I'): # del IED_
                    for k in range(len(title)):
                        title[k]=title[k][4:]

    for i in range(len(mean)):
        for k in range(len(mean[i])):
            mean[i][k]=round(mean[i][k]/(z/5),4)

    indexDict={stages[i]:{title[k]:mean[i][k] for k in range(len(title))} for i in range(len(stages))}
    return indexDict

def electrodes_map(headMap):
    headMap[1][6]="AF3"
    headMap[1][7]="AF3"
    headMap[1][-8]="AF4"
    headMap[1][-7]="AF4"

    headMap[2][3]="F7"
    headMap[2][4]="F7"
    headMap[2][-4]="F8"
    headMap[2][-5]="F8"

    headMap[2][8]="F3"
    headMap[2][9]="F3"
    headMap[2][-9]="F4"
    headMap[2][-10]="F4"

    headMap[3][4]="FC5"
    headMap[3][5]="FC5"
    headMap[3][-5]="FC6"
    headMap[3][-6]="FC6"

    headMap[4][1]="T7"
    headMap[4][2]="T7"
    headMap[4][-2]="T8"
    headMap[4][-3]="T8"

    headMap[7][4]="P7"
    headMap[7][5]="P7"
    headMap[7][-5]="P8"
    headMap[7][-6]="P8"

    headMap[8][7]="O1"
    headMap[8][8]="O1"
    headMap[8][-8]="O2"
    headMap[8][-9]="O2"

    return headMap

def resizer(HeadMap, multiple):
    for i in range(len(HeadMap)):
        nLine = []
        for k in range(len(HeadMap[i])):
            for z in range(multiple):
                nLine.append(HeadMap[i][k])
        HeadMap[i] = nLine.copy()
    newHead = []
    for i in range(len(HeadMap)):
        for k in range(multiple*3):
            newHead.append(HeadMap[i])
    return newHead

def transponate(arr):
    nArr=[]
    for i in range(len(arr[0])):
        collumn = []
        for k in range(len(arr)):
            collumn.append(arr[k][i])
        nArr.append(collumn)
    return nArr

def smoothing(HeadMap, sigma):
    for i in range(len(HeadMap)): # Gaussian smoothing
        HeadMap[i]=sp.filters.gaussian_filter(HeadMap[i], sigma = sigma, order = 0)
    HeadMap=transponate(HeadMap)
    for k in range(len(HeadMap)):
        HeadMap[k] = sp.filters.gaussian_filter(HeadMap[k], sigma=sigma, order=0)
    return transponate(HeadMap)

try:
    #indexDict = indexes_reader('C:\\Users\Dante\Downloads\Global indexes.csv')
    indexDict = indexes_reader('C:\Clusters\EEG\EEG_Clusters.csv')
    #indexDict = indexes_reader('C:\Clusters\EEG\\2.txt')
except:
    Tk().withdraw()
    path2File = askopenfilename(initialdir="C:\\Users\Dante\Desktop\Новая папка",
                               filetypes =(("CSV File", "*.csv"),("Text File", "*.txt"), ("All Files","*.*")),
                               title = "Choose a clusters file"
                               )
    if(path2File==''):
        exit(0)
    indexDict=indexes_reader(path2File)

a=[0]*24 # line in head matrix
headMap=[]
for i in range(10):
    headMap.append(a.copy())

headMap=electrodes_map(headMap)


'''''''''''''''
Max and min
'''''''''''''''
M=[]
m=[]
b=[]
for i in range(len(stages)):
    a = []
    for chrh in indexDict[stages[i]]:
        a.append(indexDict[stages[i]][chrh])
    b.append(a)
for value in b:
    M.append(max(value))
    m.append(min(value))


plt.figure(figsize=(40.0, 25.0))
for i in range(len(stages)):
    for k in range(len(rhythms)):
        plt.subplot(5, 4, i*len(rhythms)+k+1)
        meanIndexes=deepcopy(headMap)
        for channel_rhythm in indexDict[stages[i]]:
            if(channel_rhythm[-5:]==rhythms[k]): # if found current rhythm
                for headLine in meanIndexes:
                    electrodes=[z for z, x in enumerate(headLine) if x == channel_rhythm[:-6]] # search for electrode location
                    for z in range(len(electrodes)):
                        headLine[electrodes[z]]=indexDict[stages[i]][channel_rhythm] # replace each channel with value from dict
                    if(len(electrodes)>0): # if electrode was found
                        break
        meanIndexes=resizer(meanIndexes,3)
        meanIndexes=smoothing(meanIndexes,2)
        plt.imshow(meanIndexes, cmap="jet", vmax=M[i], vmin=m[i])
        if(i==0):
            plt.title(rhythms[k])
        plt.axis('off')
plt.savefig("./Images/All.tif",dpi=(300,300))
plt.show()
