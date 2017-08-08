from typing import Dict

import numpy as np
from time import sleep

stages=['Functional repose', 'First TOVA test', 'Functional load', 'Second TOVA test', 'Aftereffect']
rhythms=['Theta','Alpha','BetaL','BetaH']
channels=['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

def ABPData2Dict(Path2ABPFile: str) -> Dict[str,np.ndarray]:
    title=["Theta","Alpha","BetaL","BetaH","Gamma"]*14
    for i in range(len(channels)):
        for k in range(5):
            title[i*5+k]=channels[i]+'_'+title[i*5+k]
    title.insert(0,'sysTime')
    with open(Path2ABPFile) as file:
        Data=False
        arr=None
        for line in file:
            if(line.split(';')[0]=='stime'):  # Perhaps that first row contains ABP data
                Data=True
                continue
            if(Data):   # After found ABP data
                row=line.split(';')
                if(row[-1]=='\n'):
                    row=row[:-1]    # Take all line without last element '\n'
                if(arr is None):
                    arr = np.array(row, dtype=np.float32)   # Creating ndArray
                else:
                    arr=np.vstack((arr, np.array(row, dtype=np.float32)))   # Adding new rows
    arr=arr.transpose()    # Transpose from arr of strings to arr of columns
    d={title[i]:arr[i] for i in range(len(title))}
    delKeys=[]
    for key in d:
        if(key[-5:]=="Gamma"):  # Deleting all Gamma columns
            delKeys.append(key)
    for key in delKeys:
        del d[key]
    return d

def global_indexes(abpdict):
    title = ["Theta", "Alpha", "BetaL", "BetaH"] * 14
    for i in range(len(channels)):
        for k in range(5):
            title[i * 5 + k] = channels[i] + '_' + title[i * 5 + k]

    sumPower = 0
    for key in title:
        for stage in stages:
            sumPower += abpdict[key][stage]

    for key in title:
        for stage in stages:
            abpdict[key][stage] /= sumPower

    return abpdict



if (__name__=="__main__"):
    path = "C:\\Users\УрФУ\Desktop\ANOVA\\05.06_Сысков\Patient_AverageBandPowers.csv"
    abpDict=ABPData2Dict(path)

    '''''''''''''''''
     Time stages
    '''''''''''''''''
    if(True):
        startTime=abpDict["sysTime"][0] # First element as a start time
        for i in range(len(abpDict["sysTime"])):
            abpDict["sysTime"][i]=(abpDict["sysTime"][i]-startTime)/1000 # Normalize to start time with seconds

        stamps = [5, 8.2, 11.4, 14.6, 19.6] # Stages times
        for i in range(len(stamps)):
            stamps[i] *= 60

        if (stamps[-1] > abpDict["sysTime"][-1]): # If file has less length reduce last stage time
            stamps[-1] = abpDict["sysTime"][-2]

        stageTime = [0]
        k = 0
        for i in range(len(abpDict["sysTime"])): # Finding for the indexes which has that times
            if (abpDict["sysTime"][i] > stamps[k]):
                stageTime.append(i)
                k += 1
                if (k == len(stamps)):
                    break

        for key in abpDict:
            abpDict[key]={stages[i]:abpDict[key][i:i+1] for i in range(len(stages))}

    '''''''''''''''''
     Indexes calculating
    '''''''''''''''''
    if(True):
        for key in abpDict:
            if(key=="sysTime"):
                continue
            for stage in stages:
                abpDict = np.sum(abpDict[key][stage]) # calculating power for each stage

        abpDict=global_indexes(abpDict) # calculating global indexes

    '''''''''''''''''
     Saving to csv
    '''''''''''''''''
    if (True):
        from os import makedirs
        from os.path import exists

        path2ClustersAPB = 'C:\Clusters\ABP'
        if not exists(path2ClustersAPB):
            makedirs(path2ClustersAPB)

        clusterFileExist = False
        try:
            open(path2ClustersAPB + '\ABP features.csv', 'r')
            clusterFileExist = True
        except:
            clusterFileExist = False

        with open(path2ClustersAPB + '\ABP features.csv', 'a') as file:
            if not clusterFileExist:
                line = 'Subject;'
                for k in range(len(abpDict)-1):
                    line += columnNames[k] + ';'
                line = line[:len(line) - 1]  # all without last ';'
                line += '\n'
                file.write(line)



        for i in range(len(stages)):
            line=""
            for key in abpDict:
                if (key == "sysTime"):
                    continue
                line+=str(abpDict[key][stages])





