import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

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
    headMap[0][6]="AF3"
    headMap[0][7]="AF3"
    headMap[0][-8]="AF4"
    headMap[0][-7]="AF4"

    headMap[1][3]="F7"
    headMap[1][4]="F7"
    headMap[1][-4]="F8"
    headMap[1][-5]="F8"

    headMap[1][8]="F3"
    headMap[1][9]="F3"
    headMap[1][-9]="F4"
    headMap[1][-10]="F4"

    headMap[2][4]="FC5"
    headMap[2][5]="FC5"
    headMap[2][-5]="FC6"
    headMap[2][-6]="FC6"

    headMap[3][1]="T7"
    headMap[3][2]="T7"
    headMap[3][-2]="T8"
    headMap[3][-3]="T8"

    headMap[6][4]="P7"
    headMap[6][5]="P7"
    headMap[6][-5]="P8"
    headMap[6][-6]="P8"

    headMap[7][7]="O1"
    headMap[7][8]="O1"
    headMap[7][-8]="O2"
    headMap[7][-9]="O2"

    return headMap

try:
    indexDict = indexes_reader('C:\Clusters\EEG\EEG_Clusters.csv')
except:
    Tk().withdraw()
    path2File = askopenfilename(initialdir="C:\\Users\Dante\Desktop\Новая папка",
                               filetypes =(("CSV File", "*.csv"),("Text File", "*.txt"), ("All Files","*.*")),
                               title = "Choose a clusters file"
                               )
    indexDict=indexes_reader(path2File)




print(indexDict)
a=[0]*24 # line in head matrix
headMap=[]
for i in range(8):
    headMap.append(a.copy())

headMap=electrodes_map(headMap)

for i in range(len(stages)):
    for k in range(len(rhythms)):
        plt.subplot(5, 4, i*len(rhythms)+k+1)
        meanIndexes=headMap.copy()
        for channel_rhythm in indexDict[stages[i]]:
            if(channel_rhythm[-5:]==rhythms[k]): # if found current rhythm
                for headLine in meanIndexes:
                    while(1): # replace each channel with value from dict
                        try:
                            headLine[headLine.index(channel_rhythm[:-6])]=indexDict[stages[i]][channel_rhythm]
                        except:
                            break

        plt.imshow(meanIndexes, cmap="hot")
plt.show()