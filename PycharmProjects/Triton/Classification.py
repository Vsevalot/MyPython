import os
import datetime

def matName2Time(matName: str) -> [datetime.date,datetime.time]:
    t=datetime.time(int(matName[-12:-10]), int(matName[-9:-7]), int(matName[-6:-4]))
    d=datetime.date(int(matName[-21:-17]),int(matName[-17:-15]), int(matName[-15:-13]))
    return d,t

def reportName2Date(reportName: str) -> datetime.date:
    d=datetime.date(int("20"+reportName[-6:-4]),int(reportName[-8:-6]), int(reportName[-10:-8]))
    return d

def reportTime(strTime: str, reportPath) -> datetime.time:
    point=':' # default delimiter
    for char in strTime:
        if char=='.':
            point = strTime.split('.')
            break
    t = strTime.split(point)

    if (len(t) == 1): # if there are no delimiters in the time
        t = t[0]
        if (len(t) == 3) or (len(t) == 4):  # if time 12:33:00 in format 1233
            return datetime.time(int(t[:-2]), int(t[-2:]), 00)
        if (len(t) == 5) or (len(t) == 6):
            return datetime.time(int(t[:-4]), int(t[-4:-2]), int(t[-2:])) # if time 12:33:00 in format 123300
        print("Something goes wrong, check time format:", reportPath)
        exit(1)
    if (len(t) == 2): # if there is one delimiter in the time
        if ((len(t[0])==2)or(len(t[0])==1)) and len(t[1])==2:
            return datetime.time(int(t[0]), int(t[1]), 00)
        print("Something goes wrong, check time format:", reportPath)
        exit(1)
    if (len(t)==3): # if there are two delimiters in the time
        if ((len(t[0])==2)or(len(t[0])==1)) and len(t[1])==2 and  len(t[2])==2:
            return datetime.time(int(t[0]), int(t[1]), int(t[2]))
        print("Something goes wrong, check time format:", reportPath)
        exit(1)
    print("Something goes wrong, check time format:", reportPath)
    exit(1)

def timeDif(time1, time2 ) -> int:
    return time1.hour*3600+time1.minute*60+time1.second-(time2.hour*3600+time2.minute*60+time2.second)

def readCSV(path2csv:str)->list:
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
        for line in lines: # check for square form of the csv (the number of columns is constant in the file)
            if(len(line)!=len(lines[0])):
                squareCSV=False
                print("CSV file: "+path2csv+" does not have square form (the number of columns is changing through the file)")
                exit(1)
        if(squareCSV):
            data=[[value[i] for value in lines] for i in range(len(lines[0]))] # transpose the list to make columns elements of the list
            return data

def results2dict(results:list)->dict:
    for i in range(len(results)): # convert values from "'abc'\n" to "abc"
        for k in range(len(results[i])):
            if(results[i][k]!='' and results[i][k]!='\n'):
                if(results[i][k][0]=="'"):
                    results[i][k]=results[i][k][1:]
                if(results[i][k][-1]=='\n'):
                    results[i][k] = results[i][k][:-1]
                if(results[i][k][-1]=="'"):
                    results[i][k] = results[i][k][:-1]
            else:
                results[i]=results[i][:k]
                break
    return {"Column_"+str(i+1):results[i] for i in range(len(results))}

def stageDetector(matFile:str,reportList:list):
    matDate, matTime = matName2Time(matFile)
    dayReports=[report for report in reportsList if  reportName2Date(report)==matDate ] # compare date in mat and csv files
    for report in dayReports:
        csv=readCSV(report)
        try: # search for the first line
            int(''.join(csv[0][0].split(':')))
            startLine=0
        except:
            startLine=1 # 1 because first element is a title

        if reportTime(csv[0][startLine], report)>matTime or reportTime(csv[0][-1], report)<matTime:
            continue # if first time in the report is later or earlier than matFile - pass this report
        for i in range(startLine,len(csv[0])):
            rTime=reportTime(csv[0][i], report)
            if rTime>=matTime: # if found time which is later or equal than matFile
                if (timeDif(rTime,matTime) + 30 <= timeDif(matTime, reportTime(csv[0][i-1], report))):
                    print(matFile, rTime,csv[1][i])
                    return csv[1][i] # if i line is closer to the matTime return i line
                else:
                    print(matFile, reportTime(csv[0][i-1], report), csv[1][i-1])
                    return csv[1][i-1] # else return previous line because it's closer to the matTime
    return None # if none report in reportList much return None


if __name__ == "__main__":
    path2results="E:\\test\\results.csv"
    data=readCSV(path2results)
    results=results2dict(data)

    path2reports="E:\\test\Repotrs\complete"
    reportsList = [ os.path.join(path2reports, f) for f in os.listdir(path2reports) if os.path.isfile(os.path.join(path2reports, f))]

    column="Column_4"
    for i in range(len((results[column]))):
        if stageDetector(results[column][i],reportsList):
            continue
            #print(results[column][i],stageDetector(results[column][i],reportsList))

