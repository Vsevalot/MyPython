import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
from copy import deepcopy
import scipy.io

def min_with_none(arr):
    x=9999999999999
    for i in range(len(arr)):
        if(arr[i] is None):
            continue
        if(arr[i]<x):
            x=arr[i]
    return x

def sitxls2arr(path2file):
    arr=[]
    with open(path2file,'r') as file:
        i=0
        while(1):
            arr.append(file.readline().split(';'))
            if(arr[i]==['']):
                arr=arr[:-1]
                break
            i+=1
        file.close()

    if(arr[0]==["320","240\n"]):
        arr=arr[1:]
    for i in range(len(arr)):
        if(arr[i][-1][-1]=='\n'):
            arr[i][-1]=arr[i][-1][:-1]
        for k in range(len(arr[i])):
            z = 0
            for z in range(len(arr[i][k])):
                if(arr[i][k][z]==','):
                    break
                z+=1
            if(z==0):
                arr[i][k]=float(arr[i][k])
            else:
                arr[i][k]=float(arr[i][k][:z]+'.'+arr[i][k][z+1:])

    if(len(arr)!=320) and (len(arr[0]!=240)):
        print("Warning! Files should have resolution 320x240!")
    return arr

def folderSorter(foldersArr):
    arr=[]
    for i in range(len(foldersArr)):
        arr.append(foldersArr[i][8:]) # take only number from RealtimeX
    try:
        arr[0]=int(arr[0])
    except:
        print("Can't convert folders number to int: "+arr[0])
        exit(33)

    sort=True
    for i in range(1,len(arr),1):
        arr[i]=int(arr[i])
        if(arr[i]<arr[i-1]):
            sort = False
    if(sort):
        return foldersArr
    else:
        sortArr=[]
        for i in range(len(arr)):
            m=min_with_none(arr)
            sortArr.append(foldersArr[arr.index(m)])
            arr[arr.index(m)]=None
            if (all(i is None for i in arr)):
                return sortArr

def fileSorter(filesArr):
    arr = []
    for i in range(len(filesArr)):
        arr.append(filesArr[i][1:7]) # take only number from ixxxxxx.sit.csv
    try:
        arr[0] = int(arr[0])
    except:
        print("Can't convert file number to int: " + arr[0])
        exit(33)

    sort = True
    for i in range(1, len(arr), 1):
        arr[i] = int(arr[i])
        if (arr[i] < arr[i - 1]):
            sort = False
    if (sort):
        return filesArr
    else:
        sortArr = []
        for i in range(len(arr)):
            m = min_with_none(arr)
            sortArr.append(filesArr[arr.index(m)])
            arr[arr.index(m)] = None
            if (all(i is None for i in arr)):
                return sortArr


'''''''''''''''
 Start
'''''''''''''''
try: # Fast way without dialog window
    path2folder='' # Paste path to the folder with RealtimeX files
    foldersList = [f for f in os.listdir(path2folder) if not os.path.isfile(os.path.join(path2folder, f))]
except:
    Tk().withdraw()
    path2folder = askdirectory(title="Choose a folder with RealtimeX folders")
    if (path2folder == ''):
        print("Goodbye")
        exit(0)
    foldersList = [f for f in os.listdir(path2folder) if not os.path.isfile(os.path.join(path2folder, f))]


'''''''''''''''
 Preparing files
'''''''''''''''

foldersNames=[]
for i in range(len(foldersList)):
    if(foldersList[i][:8]=="Realtime"):
        foldersNames.append(foldersList[i])
if(foldersNames==[]):
    print("Can not find any RealtimeX folder at the "+path2folder+" path")
    print("Please check the directory, it must contain RealtimeX folders")
foldersNames=folderSorter(foldersNames)


'''''''''''''''
 Writing to dictionary
'''''''''''''''

matDict={}
for i in range(len(foldersNames)):
    currentFolder=os.path.join(path2folder, foldersNames[i])
    fileList=[f for f in os.listdir(currentFolder) if os.path.isfile(os.path.join(currentFolder, f))]
    csvList=[]
    for k in range(len(fileList)):
        if (fileList[k][0]=='i') and (fileList[k][7:]==".sit.csv"):
            csvList.append(fileList[k])
    if(csvList==[]):
        print("Can not find any ixxxxxx.sit.csv file at the "+foldersNames[i]+" folder")
        print("Please, remove or rename this folder")
        exit(33)
    csvList=fileSorter(csvList)
    arr=[]
    for k in range(len(csvList)):
        print(round((k+1+i*len(csvList))*100/(len(csvList)*len(foldersNames)),2),"% completed, working with "+ foldersNames[i] + " folder")
        arr.append(sitxls2arr(os.path.join(currentFolder,csvList[k])))
    if(i<len(foldersNames)-1):
        print("\nPreparing to the next stage\n")
    else:
        print("\nSaving to .mat file\n")
    matDict[foldersNames[i]]=deepcopy(arr)


'''''''''''''''
 Saving
'''''''''''''''

path2save="realtime.mat" # Do not forgot to add "name.mat" to the end of the path
scipy.io.savemat(path2save,matDict)
print("Completed")