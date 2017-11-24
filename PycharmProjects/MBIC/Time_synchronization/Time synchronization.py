import os
import sys

def xls2dict(path):
    table = []
    with open(path, "r") as myfile:
        for line in myfile:
            l = line.strip().split('\t')
            table.append(l)

    columns = []
    column = []
    table1 = []
    intline = []
    for i in range(1, len(table), 1):
        for k in range(len(table[i])):
            try:
                intline.append(int(table[i][k]))
            except ValueError:
                intline.append(table[i][k])
        table1.append(intline)
        intline = []

    for k in range(len(table[0])):
        for i in range(len(table1)):
            column.append(table1[i][k])
        columns.append(column)
        column = []

    value_dict = {table[0][z]: columns[z] for z in range(len(table[0]))} # build a dictionary with titles of columns as keys
    return value_dict

def Epoc_xls2dict(path):
    table = []
    with open(path, "r") as myfile:
        i=0
        for line in myfile:
            if ((i==0) or (i==1)): # empty lines
                i+=1
                continue
            elif(i==10000):
                break
            l = line.strip().split(';')
            table.append(l)
            i+=1

    columns = []
    column = []
    table1 = []
    intline = []
    for i in range(1, len(table), 1):
        for k in range(len(table[i])):
            if(table[i][k]!=''):
                intline.append(float(table[i][k]))
        table1.append(intline)
        intline = []

    for k in range(len(table[0])):
        for i in range(len(table1)):
            column.append(table1[i][k])
        columns.append(column)
        column = []

    value_dict = {table[0][z]: columns[z] for z in range(len(table[0]))} # build a dictionary with titles of columns as keys
    return value_dict

def VSR2dict(path):
    table = []
    with open(path, "r") as myfile:
        i=0
        for line in myfile:
            if (i<26): # empty lines
                i+=1
                continue
            elif(i==2000):
                break
            l = line.strip().split('\t')
            table.append(l)
            i+=1

    columns = []
    column = []
    table1 = []
    intline = []
    for i in range(1, len(table), 1):
        for k in range(len(table[i])):
            try:
                intline.append(int(table[i][k]))
            except ValueError:
                intline.append(table[i][k])
        table1.append(intline)
        intline = []

    for k in range(len(table[0])):
        for i in range(len(table1)):
            column.append(table1[i][k])
        columns.append(column)
        column = []

    value_dict = {table[0][z]: columns[z] for z in range(len(table[0]))} # build a dictionary with titles of columns as keys
    return value_dict

# finding files
mypath='C:'+'\\'+'Users\Dante\Desktop\HomeWork'+'\\'+'05.06_Сысков'
print(mypath)
filelist=[]
filenames = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
for i in range(len(filenames)):
    filelist.append(mypath+'\\'+filenames[i])

print(filelist)

lf=0 # last file
for i in range(len(filelist)):
    if lf<=os.path.getctime(filelist[i]):
        lf=os.path.getctime(filelist[i]) # finding the latest file

for i in range(len(filelist)):
    if lf==os.path.getctime(filelist[i]):
        latest=filelist[i] # finding the latest file's name
        break

#print("The latest file time is: ", round(lf*1000))

pc='D:\Epoc+\PatientsCodes.txt'# path to patients' codes table
#print(xls2dict(pc))

patients_files=[]
patient_name='Сысков'
VSRd=VSR2dict(filelist[0])
EEGd=Epoc_xls2dict(filelist[2])
MDd=Epoc_xls2dict(filelist[3])
#print(Epoc_xls2dict(filelist[1])) should change Epoc_xls2dict to make label like 'AF-3-Tetha'

start_time=max([EEGd['stime'][0],MDd['stime '][0]])+10000 # from 10 second after latest start

i=0
k=0
while(1):
    if(EEGd['stime'][i])>start_time:
        break
    i+=1

while(1):
    if(MDd['stime '][k])>start_time:
        break
    k+=1

def stupidMatLab(path):
    table = []
    with open(path, "r") as myfile:
        for line in myfile:
            l = line.strip().split(',')
            table.append(l)

    columns = []
    column = []
    table1 = []
    intline = []
    for i in range(0, len(table), 1):
        for k in range(len(table[i])):
            try:
                intline.append(float(table[i][k]))
            except ValueError:
                intline.append(table[i][k])
        table1.append(intline)
        intline = []

    for k in range(len(table[0])):
        for i in range(len(table1)):
            column.append(table1[i][k])
        columns.append(column)
        column = []
    lable=[['useless','ma','mg']]
    value_dict = {lable[0][z]: columns[z] for z in range(len(table[0]))}  # build a dictionary with titles of columns as keys
    return value_dict

p='C:'+'\\'+'Users\Dante\Desktop'+'\\'+'Untitled Project\csvlist.dat'

filttt=stupidMatLab(p)

def mean(arr):
    s=0
    for i in arr:
       s+=i
    return s/len(arr)

import numpy as np
#print(np.std(filttt['ma']))
lable=[]
for key in EEGd:
    lable.append(key)
final_EEG = {lable[z]: EEGd[lable[z]][i:]for z in range(len(EEGd))}  # build a dictionary with titles of columns as keys
final_MD = {'stime':MDd['stime '][k:],'ma':filttt['ma'][k-1:],'mg':filttt['mg'][k-1:]}

for i in range(len(final_EEG['stime'])):
    final_EEG['stime'][i]-=start_time
    final_EEG['stime'][i] = int(round(final_EEG['stime'][i]))

final_EEG.pop(' IED_COUNTER',0)
final_EEG.pop(' IED_TIMESTAMP',0)
final_EEG.pop(' IED_INTERPOLATED',0)
final_EEG.pop(' IED_MARKER',0)
final_EEG.pop(' IED_RAW_CQ',0)
final_EEG.pop(' IED_GYROX',0)
final_EEG.pop(' IED_GYROY',0)
final_EEG.pop(' IED_COUNTER',0)


for i in range(len(final_MD['stime'])):
    final_MD['stime'][i]-=start_time
    final_MD['stime'][i] = int(round(final_MD['stime'][i]))

del EEGd
del MDd
del VSRd
del filttt

i=0
k=0

mean_eeg={key: mean(final_EEG[key]) for key in final_EEG}
std_eeg={key: np.std(final_EEG[key]) for key in final_EEG}
mean_md={'ma': mean(final_MD['ma']), 'mg':mean(final_MD['mg'])}
std_md={'ma': np.std(final_MD['ma']), 'mg':np.std(final_MD['mg'])}

toohighm={key:mean_md[key]+3*std_md[key] for key in mean_md}
toolowm={key:mean_md[key]-3*std_md[key] for key in mean_md}

art_times=[]
true_art={key:[] for key in final_EEG}
true_art.pop('stime',0)


for i in range(len(final_MD['stime'])):
    if (((final_MD['ma'][i]>toohighm['ma']) or (final_MD['ma'][i]<toolowm['ma'])) or ((final_MD['mg'][i]>toohighm['mg']) or(final_MD['mg'][i]<toolowm['mg']))):
        art_times.append(final_MD['stime'][i])

toohighE={key:mean_eeg[key]+3*std_eeg[key] for key in true_art}
toolowE={key:mean_eeg[key]-3*std_eeg[key] for key in true_art}

t=0 # delete duplicates
while(t<len(art_times)):
    if art_times[t]==art_times[t-1]:
        del art_times[t]
        continue
    t+=1

t=0 # delite x+1 near x
while(t<len(art_times)):
    if (art_times[t]==art_times[t-1]+1):
        del art_times[t]
        continue
    t+=1

check_list={key:0 for key in true_art}

print(art_times)
k=0

def inrange(arr, iterator, number):
    span=150
    bot=arr[iterator]-span
    top=arr[iterator]+span
    if ((bot<number) and (top>number)):
        return True
    else:
        return False

i=0

for i in range(len(final_EEG['stime'])):
   while(1):
       if art_times[k+1]<final_EEG['stime'][i]:
           k+=1
       else:
           break
   if (inrange(final_EEG['stime'],i,art_times[k])):
       z=i
       while(inrange(final_EEG['stime'],z,art_times[k+1])or(final_EEG['stime'][z]<final_EEG['stime'][z]+1000)):
           for key in true_art:
               if ((final_EEG[key][z]>toohighE[key]) or (final_EEG[key][z]<toolowE[key]) and (check_list[key]==0)):
                   true_art[key].append(final_EEG['stime'][z])
                   check_list[key]=1
           if all(check_list[ky]==1 for ky in check_list):
               break
           if z==len(final_EEG['stime'])-1:
               break
           z+=1
       k+=1
       if (k>=len(art_times)-1):
           break
   for ky in check_list:
       check_list[ky]=0 # refresh checklist



ndict={key:[0] for key in true_art}

for key in true_art:
    i=0
    k=0
    while(i<(len(true_art[key]))):
        if true_art[key][i]>100+ndict[key][k]:
            ndict[key].append(true_art[key][i])
            k+=1
        i+=1

print(ndict)

strarr=[]
s=''
for key in ndict:
    s+=key
    for i in range(len(ndict[key])):
        s+=str(ndict[key][i])+';'
    s+='\n'
    strarr.append(s)
    print(s)
    s=''

with open("EEG_ART.txt", "w") as text_file:
    for line in strarr:
        text_file.write(line)