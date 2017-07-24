import csv
csv_protocol = open("Work_protocol"+".csv",'r')
readCSV=csv.reader(csv_protocol, delimiter=';')
patients=[]
for row in readCSV:
    patients.append(row)

for i in range(0, len(patients)):
    for k in range(1, len(patients[i])-1):
        patients[i][k]=int(patients[i][k])

#print(patients)
csv_protocol.close()

# this function returns first name in "first_name second_name" string
def first_name(string):
    fname=""
    for ch in string:
        if(ch==" "):
            break
        fname+=ch
    return fname

# this function returns time in row in ms
def EEG_time(string):
    time=""
    for ch in string:
        if(ch==";"):
            break
        time+=ch
    return int(time)

# this function returns number of patient in protocol
def find_patient(patient):
    for i in range(len(patients)):
        if (first_name(patients[i][0]) == patient):
            return i
    return -1 # if there is not a patient with this first name in the protocol

def take_timings(patient):
    number=find_patient(patient)
    t=[]
    for i in range(2, 6):
        t.append(patients[number][i])
    return t

import os

patient="Гаврилова"
patient_number=find_patient(patient) # number of patient
patient_timings=take_timings(patient) # array type [15, 30, 44 ... ] to separate EEG section

string_cor="" # corrected string
csvFile = open(patient+".csv",'w')
string="wow"
with open(patient+'.txt') as txtFile:
    i=0
    string = txtFile.readline()
    while(len(string)):# если закончилось чтение
        i+=1
        string=txtFile.readline()
        if(i<96): # Первые 97 строк содержат общую информацию
            continue
        for ch in range(0,len(string),1): # переписываем в более корректную форму (с заменой разделителей)
            if(string[ch]=='\t'):
                string_cor += ';'
                continue
            if(string[ch]==',' and string[ch-1]=='\t'): # замена запятой на минус (баг проги энцефалографа)
                string_cor += '-'
                continue
            if(string[ch]==','):
                string_cor+='.'
                continue
            string_cor+=string[ch] # записываем корректную строку
        #print(string_cor)
        csvFile.write(string_cor)# запись корректной строки в csv
        try:
            if any(EEG_time(string_cor)== k for k in patient_timings):
                csvFile.write(12*'1;'+'\n')  # запись пустой строки в csv для разделения секций ээг
        except ValueError:
            if(string_cor==""):
                print("Rendering 'txt' to 'cvs' is completed")
            else:
                print("There is some trouble at ",(i-97)*4, " ms")
        string_cor=""


csvFile.close()




















