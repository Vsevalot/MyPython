import os

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

def Motion_Data_2_Dict(Path2MotionFile):
    notanumber = True
    label = ''
    value = []
    with open(Path2MotionFile) as file:
        while (notanumber):  # read until find numbers, previous line - label
            line = file.readline()
            if ((line == '\n') or (line == '')):
                continue
            line = line.split(';')
            while ((line[-1][-1] == '\n') or ((line[-1] == ''))):
                newitem = ''
                for i in range(len(line[-1]) - 1):
                    newitem += line[-1][i]
                del line[-1]
                if (len(newitem)):
                    line.append(newitem)
            try:
                for i in range(len(line)):
                    line[i] = float(line[i])
                value.append(line)
                notanumber = False
            except(ValueError):
                label = line
                for i in range(len(label)):
                    newitem = ''
                    for letter in label[i]:
                        if letter == ' ':
                            continue
                        newitem += letter
                    label[i] = newitem

        while (len(line)):
            line = file.readline()
            if ((line == '\n') or (line == '')):
                continue
            line = line.split(';')
            while ((line[-1][-1] == '\n') or ((line[-1] == '')) or (line[-1] == '\n')):
                newitem = ''
                for i in range(len(line[-1]) - 1):
                    newitem += line[-1][i]
                del line[-1]
                if (len(newitem)):
                    line.append(newitem)
            for i in range(len(line)):
                line[i] = float(line[i])
            value.append(line)

        cvalue = []
        for i in range(len(value[0])):
            column = []
            for k in range(len(value)):
                column.append(value[k][i])
            cvalue.append(column)

        if (len(label) == len(cvalue)):
            valuedict = {label[i]: cvalue[i] for i in range(len(label))}
            return valuedict
        else:
            print("Something goes wrong, check number of labels and number of data columns")
            exit(33)

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
            intline.append(int(table[i][k]))
        table1.append(intline)
        intline = []

    for k in range(len(table[0])):
        for i in range(len(table1)):
            column.append(table1[i][k])
        columns.append(column)
        column = []

    value_dict = {table[0][z]: columns[z] for z in
                  range(len(table[0]))}  # build a dictionary with titles of columns as keys
    return value_dict


with open("whoIsYourDaddy.csv") as timeFile: # reading all files times
    fileNames=[]
    fileTimes=[]
    for line in timeFile:
        fileNames.append(line.split(';')[0]) # file name
        fileTimes.append(float(line.split(';')[1][:-1])) # time without '\n'
    timeDict={fileNames[i]:fileTimes[i] for i in range(len(fileNames))}

print(timeDict)

# finding files
tovaPath='C:\\Users\Dante\Desktop\EpocData\\Пуртов_0906\\toav-14_11.xls'
eegPath='C:\\Users\Dante\Desktop\EpocData\\Пуртов_0906\\Patient_EEG.csv'
mdPath='C:\\Users\Dante\Desktop\EpocData\\Пуртов_0906\\Patient_MotionData.csv'
tTime=0
eTime=(round(os.path.getctime(eegPath) - os.path.getctime(tovaPath),3))*1000
mTime=(round(os.path.getctime(mdPath)-os.path.getctime(tovaPath),3))*1000
print(tTime,eTime,mTime)
print(1497007597057)