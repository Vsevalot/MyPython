import os
import datetime
import matplotlib as x
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

def matName2Time(matName: str) -> [datetime.date,datetime.time]: # convert Mat file's name to date and time
    opening=matName.index('(')
    closing=matName.index(')')
    timeDelta=30*int(matName[opening+1:closing])
    matName=matName[:opening]
    t=datetime.timedelta(hours=int(matName[-12:-10]), minutes=int(matName[-9:-7]), seconds=int(matName[-6:-4])+timeDelta)
    d=datetime.date(int(matName[-21:-17]),int(matName[-17:-15]), int(matName[-15:-13]))+t # if t has more than 23:59:59 so one day will be added
    m,s=divmod(t.seconds, 60)
    h,m=divmod(m, 60)
    t=datetime.time(h,m,s)
    return d,t

def reportName2Date(reportName: str) -> datetime.date: # convert report's Name to date
    d=datetime.date(int("20"+reportName[-6:-4]),int(reportName[-8:-6]), int(reportName[-10:-8]))
    return d

def reportTime(strTime: str, reportPath: str) -> datetime.time: # convert string to time in the given report
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
        if (len(t[0])==2 or len(t[0])==1) and len(t[1])==2:
            return datetime.time(int(t[0]), int(t[1]), 00)
        print("Something goes wrong, check time format:", reportPath)
        exit(1)
    if (len(t)==3): # if there are two delimiters in the time
        if (len(t[0])==2 or len(t[0])==1) and len(t[1])==2 and  len(t[2])==2:
            return datetime.time(int(t[0]), int(t[1]), int(t[2]))
        print("Something goes wrong, check time format:", reportPath)
        exit(1)
    print("Something goes wrong, check time format:", reportPath)
    exit(1)

def timeDif(time1, time2 ) -> int: # calculate difference between to times in seconds
    return time1.hour*3600+time1.minute*60+time1.second-(time2.hour*3600+time2.minute*60+time2.second)

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

def results2dict(results:list) -> dict: # convert values from "'abc'\n" to "abc"
    for i in range(len(results)):
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

def stageDetector(matFile:str,reportList:list): # search for the closest time to the MatFile in all reports and return stage in this time
    matDate, matTime = matName2Time(matFile)
    dayReports=[report for report in reportsList if  reportName2Date(report)==matDate ] # compare date in mat and csv files
    def chronoChecker(times:list, report:str)->bool: # Check the correct order in the given time list
        for time in range(1,len(times)):
            if timeDif(times[time],times[time-1])<0:
                print("Wrong time order check file:", report)
                return False
        return True

    '''''''''''''''''
    # Search for the correct by time report
    '''''''''''''''''
    for report in dayReports:
        csv=readCSV(report)
        try: # search for the first line
            float(''.join(csv[0][0].split(':')))
            startLine=0
        except:
            startLine=1 # 1 because first element is a title
        if reportTime(csv[0][startLine], report)>matTime or reportTime(csv[0][-1], report)<matTime:
            continue # if first time in the report is later or earlier than matFile - pass this report

        '''''''''''''''''
        # Search for the closest stage
        '''''''''''''''''
        rTimes=[]
        for i in range(startLine,len(csv[0])): # This line is reached if the correct report is found
            rTimes.append(reportTime(csv[0][i], report))

        if(chronoChecker(rTimes, report)): # If all times if file are in correct order
            for i in range(len(rTimes)):
                if rTimes[i]>=matTime: # if found time which is later or equal than matFile
                    if (timeDif(rTimes[i],matTime)+30 <= timeDif(matTime, rTimes[i-1])) : # +30 seconds because the algorithm has a delay
                        #print(matTime, rTimes[i],csv[1][i])
                        return csv[1][i] # if i line is closer to the matTime return i line
                    else:
                        #print(matTime, rTimes[i-1], csv[1][i-1])
                        return csv[1][i-1] # else return previous line because it's closer to the matTime
        else:
            break
    return None # if none report in reportList much return None

if __name__ == "__main__":
    '''''''''''''''''
    # Preparing files
    '''''''''''''''''
    try:
        path2results = "E:\\test\\results.csv"
        results = results2dict(readCSV(path2results))
        path2reports = "E:\\test\\Reports\complete"
        reportsList = [os.path.join(path2reports, f) for f in os.listdir(path2reports) if
                       os.path.isfile(os.path.join(path2reports, f))]
    except:
        '''''''''''''''''
        # Results file window
        '''''''''''''''''
        Tk().withdraw()
        path2results = askopenfilename(initialdir="C:\\",
                                    filetype=(("CSV File", "*.csv"), ("All Files","*.*")),
                                    title="Choose a file with results of classification")
        if (path2results == ''):
            exit(0)
        results = results2dict(readCSV(path2results))


        '''''''''''''''''
        # Reports folder window
        '''''''''''''''''
        Tk().withdraw()
        path2reports = askdirectory(initialdir="C:\\",
                                    title="Choose a folder which contain reports")
        if (path2reports == ''):
            exit(0)
        reportsList = [os.path.join(path2reports, f) for f in os.listdir(path2reports) if
                       os.path.isfile(os.path.join(path2reports, f))]

    '''''''''''''''''
    # Data collection
    '''''''''''''''''
    histValue=[]
    columns=list(results.keys())
    parts=[] # To calculate a percentage of processed files for each column
    for column in range(len(columns)):
        histValue.append([])
        for matFile in results[columns[column]]:
            histValue[column].append(stageDetector(matFile,reportsList)) # returns None if can't find time from a mat file
        parts.append(len(histValue[column]))
        histValue[column] = [ int(v) for v in histValue[column] if v is not None] # v[:1] to convert "3\n" to '3'
        parts[column]=int(100*round(len(histValue[column])/parts[column],2))



    percentage=[]
    k=1
    for usedPart in parts:
        for i in range(usedPart):
            percentage.append(k)
        k+=1

    bar_locations = [-1,0,1,2,3,4,5]
    histPer=[[int(100*round(column.count(i)/len(column),2)) for i in bar_locations] for column in histValue]



    '''''''''''''''''
    # Plotting
    '''''''''''''''''
    x.rcParams.update({'font.size': 22})
    plt.figure(figsize=(40.0, 25.0))
    for column in range(len(columns)):
        a=plt.subplot(2,2,column+1)
        plt.bar(bar_locations,histPer[column],align='center')
        plt.title("Anesthesia stage distribution for the group "+str(column+1))
        #plt.xlabel("Stage")
        plt.ylabel("Percentage")
        names = ["Artifacts", "Wakefulness", "First stage", "Second stage", "Third stage","Fourth stage", "Fifth stage"]
        #a.set_xticks(bar_locations)
        a.set_xticklabels(names)
        plt.axis([-0.5, 6, 0,100])

    a=plt.subplot(2, 2, 4)
    plt.hist(percentage, color='r')
    plt.title("Percentage of use mat files for the each group")
    plt.xlabel("Group (column)")
    plt.ylabel("Percentage")
    plt.axis([0.5, 3.5, 0, 100])
    #names = ["First column", "Second column","Third column"]
    #a.set_xticks([ 1, 2, 3])
    #a.set_xticklabels(names)
    #plt.show()
    plt.savefig("E:\\test\\PercentageHist.jpg", dpi=300)


