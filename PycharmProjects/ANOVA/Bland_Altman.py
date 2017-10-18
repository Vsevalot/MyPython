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
import numpy as np
import matplotlib as x

def bland_altman_plot(data1, data2, *args, **kwargs):
    data1     = np.asarray(data1)
    data2     = np.asarray(data2)
    mean      = np.mean([data1, data2], axis=0)
    diff      = data1 - data2                   # Difference between data1 and data2
    md        = np.mean(diff)                   # Mean of the difference
    sd        = np.std(diff, axis=0)            # Standard deviation of the difference

    plt.scatter(mean, diff, *args, **kwargs)
    plt.axhline(md,           color='red')
    plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96*sd, color='gray', linestyle='--')

path2EPO="C:\ANOVA\AlphaTheta.csv"
path2ENC="C:\ANOVA\AlphaThetaEnc.csv"

enc=readCSV(path2ENC)
epo=readCSV(path2EPO)


enc=[[float(v) for v in column] for column in enc]
epo=[[float(v) for v in column[:7]] for column in epo]

channels=['f3f1','f4a2','c3a1','c4a2','p3a1','p4a2','o1a1','o2a2','a1a2']
rhythms=['Theta','Alpha','BetaL','BetaH']
stages= ['Background', 'First TOVA test', 'Hyperventilation', 'Second TOVA test', 'Aftereffect']

x.rcParams.update({'font.size': 16})
csfont = {'fontname':'Times New Roman'}
plt.figure(figsize=(40.0, 25.0))
# for i in range(5):
#     plt.subplot(2, 5, i + 1)
#     bland_altman_plot(enc[2*i],epo[2*i])
#     plt.title("Alpha/Theta "+ '('+stages[i]+')')
# for i in range(5):
#     plt.subplot(2, 5, i + 6)
#     bland_altman_plot(enc[2*i+1],epo[2*i+1])
#     plt.title("Beta/Theta " + '('+stages[i]+')')
#
#
# plt.show()

plt.subplot(2, 2, 1)
bland_altman_plot(enc[2], epo[2])
plt.title("Alpha/Theta " + '(' + stages[2] + ')',**csfont)
plt.subplot(2, 2, 2)
bland_altman_plot(enc[4], epo[4])
plt.title("Alpha/Theta " + '(' + stages[3] + ')',**csfont)
plt.subplot(2, 2, 3)
bland_altman_plot(enc[3], epo[3])
plt.title("Beta/Theta " + '(' + stages[2] + ')',**csfont)
plt.subplot(2, 2, 4)
bland_altman_plot(enc[5], epo[5])
plt.title("Beta/Theta " + '(' + stages[2] + ')',**csfont)
plt.show()
