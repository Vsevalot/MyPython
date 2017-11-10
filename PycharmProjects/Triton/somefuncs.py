import os
import datetime
import matplotlib as x
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

def matName2Time(matName: str) -> [datetime.date,datetime.time]: # convert Mat file's name to date and time
    before=matName.split('(')
    timeDelta=30*int(before[1].split(')')[0])
    matName=before[0]
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
        if char=='-':
            point = strTime.split('-')
            break
    t = strTime.split(point)
    try:
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
    except:
        print("Something goes wrong, check time format:", reportPath)
        exit(1)

def timeDif(time1, time2 ) -> int: # calculate difference between to times in seconds
    return time1.hour*3600+time1.minute*60+time1.second-(time2.hour*3600+time2.minute*60+time2.second)

def readCSV(path2csv:str) -> list: # read any CSV file and return it like list of columns
    with open(path2csv, 'r') as file:
        lines=[[v for v in line.split(';') if v!='\n'] for line in file.readlines()] # reading all lines in the file with rows as elements of the list
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
            for v in data[-1]:
                if v!='\t':
                    return data
            return data[:-1]

def readXLSX(path2xlsx:str)->list:
    from openpyxl import load_workbook
    wb = load_workbook(filename=path2xlsx, read_only=True)
    ws = wb[wb.get_sheet_names()[0]]
    lines = []
    for row in ws.rows:
        line = []
        for cell in row:
            if cell.value is not None:
                line.append(str(cell.value))
            else:
                line.append('')
        lines.append(line)
    return [[line[i] for line in lines if line[i] is not None] for i in range(len(lines[0]))]

def results2dict(results:list) -> dict: # convert values from "'abc'\n" to "abc"
    for i in range(len(results)):
        for k in range(len(results[i])):
            if(results[i][k]!='' and results[i][k]!='\n' and results[i][k]!='\t'):
                if(results[i][k][0]=="'"):
                    results[i][k]=results[i][k][1:]
                if(results[i][k][-1]=='\n'):
                    results[i][k] = results[i][k][:-1]
                if(results[i][k][-1]=="'"):
                    results[i][k] = results[i][k][:-1]
                if (results[i][k][0] == '\t'):
                    results[i][k] = results[i][k][1:]
            else:
                results[i]=results[i][:k]
                break
    return {"Column_"+str(i+1):results[i] for i in range(len(results))}

def stageDetector(matFile:str,reportList:list,fiveMinutes:bool=None): # search for the closest time to the MatFile in all reports and return stage in this time
    matDate, matTime = matName2Time(matFile)
    dayReports=[report for report in reportsList if  reportName2Date(report)==matDate ] # compare date in mat and csv files
    def chronoChecker(times:list, report:str)->bool: # Check the correct order in the given time list
        for time in range(1,len(times)):
            if timeDif(times[time],times[time-1])<0:
                print("Wrong time order check file:", report, times[time],'<',times[time-1])
                exit(0)
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
            if fiveMinutes:
                for i in range(len(rTimes)):
                    if rTimes[i] >= matTime:  # if found time which is later or equal than matFile
                        stages = {str(stage):0 for stage in [-1, 0, 1, 2, 3, 4, 5, 6, 7]}
                        stages[csv[1][i]]+=timeDif(rTimes[i],matTime)
                        k=i+1
                        if (k == len(rTimes)):
                            return csv[1][i]
                        while (timeDif(rTimes[k],matTime)<300):
                            stages[csv[1][k]]+=timeDif(rTimes[k],rTimes[k-1])
                            k+=1
                            if k == len(rTimes):
                                k-=1
                                break
                        if sum([stages[stage] for stage in stages])<300:
                            stages[csv[1][k]]+=300-timeDif(rTimes[k-1],matTime)
                        return max(stages, key=stages.get)

            for i in range(len(rTimes)):
                if rTimes[i]>=matTime: # if found time which is later or equal than matFile
                    if (timeDif(rTimes[i],matTime)+30 <= timeDif(matTime, rTimes[i-1])) : # +30 seconds because the algorithm has a delay
                        return csv[1][i] # if i line is closer to the matTime return i line
                    else:
                        return csv[1][i-1] # else return previous line because it's closer to the matTime
        else:
            break
    return None # if none report in reportList much return None

def groupStatistic(res:dict,reportsList): # take results of classification as dictionary and return list of percentages and list of percentages of used matFiles
    histValue=[]
    columns=list(res.keys())
    def stageLen():
        for column in res:
            for matName in res[column]:
                if matName[-2:-1]!='0':
                    return False
        return True
    fiveMinutesFragments=stageLen()
    parts=[] # To calculate a percentage of processed files for each column
    strangeFiles=[]
    for column in range(len(columns)):
        histValue.append([])
        for matFile in res[columns[column]]:
            histValue[column].append(stageDetector(matFile,reportsList,fiveMinutesFragments)) # returns None if can't find time from a mat file
            if (column==6-1) and (histValue[6-1][-1]=='0'):
                strangeFiles.append(matFile)
        if (histValue[column]!=[]):
            parts.append(int(100*(len(histValue[column])-histValue[column].count(None))/len(histValue[column])))
            histValue[column] = [ int(v) for v in histValue[column] if (v is not None) and (v != "4") and (v != "5") and (v != "6") and (v != "7")] # and (v != "-1")
        else:
            parts.append(0)
    stages=[]
    for column in histValue:
        for stage in column:
            if stage not in stages:
                stages.append(stage)
    stages=sorted(stages)
    files=sum(histValue,[])
    files=[round(100*files.count(i)/len(files),2) for i in stages]
    histPer=[[round(100*column.count(i)/sum([len(column) for column in histValue]),2) for i in stages] for column in histValue]
    return histPer, parts, files, strangeFiles, stages

def recSubPlotDet(plotNumber:int):
    n=plotNumber
    factors=[]
    i=2
    while(n!=1): # feed factors arr with factors 18 = [2,3,3]
       if n%i==0:
           factors.append(i)
           n/=i
       else:
           i+=1

    if len(factors)==1: # we need a rectangular subplot, so 3*1 is not enough -> 2*2
        return recSubPlotDet(plotNumber+1)
    if len(factors)>2:
        i=0
        while(len(factors)!=2):
            factors[i%2]*=factors[-1]
            i+=1
            factors.pop(-1)
    if(factors[1]<factors[0]): # if width < high swap them
        return factors[1], factors[0]
    return factors[0], factors[1]

def fileName(path2file:str)->str:
    for i in range(len(path2file)-1,-1,-1):
        if path2file[i]=='.':
            path2file=path2file[:i]
            break
    for i in range(len(path2file)-1,-1,-1):
        if path2file[i]=='\\':
            path2file=path2file[i+1:]
            break
    return path2file

def write2csv(some2Dlist:list, path2save:str):
    if type(some2Dlist[0])!=list:
        print("You should give a list of lists to write it for csv")
        exit(0)
    try:
        with open(path2save, 'w') as file:
            for k in range(max([len(l) for l in some2Dlist])):
                line=''
                for column in some2Dlist:
                    if k>=len(column):
                        line+=';'
                    else:
                        line+=column[k]+';'
                file.write(line[:-1]+'\n')
            file.close()
        print("Saved : "+path2save)
        return True
    except:
        return False


if __name__ == "__main__":
    '''''''''''''''''
    # Preparing files
    '''''''''''''''''
    try:
        path2results = "Z:\\Tetervak\\21_data14_8_5min_20171110_110000.csv"
        if (path2results[-4:]=="xlsx"):
            results = results2dict(readXLSX(path2results))
        if (path2results[-3:]=="csv"):
            results = results2dict(readCSV(path2results))
        path2reports = "E:\\test\\Reports\\complete"
        reportsList = [os.path.join(path2reports, f) for f in os.listdir(path2reports) if
                       os.path.isfile(os.path.join(path2reports, f))]
    except:
        '''''''''''''''''
        # Results file window
        '''''''''''''''''
        Tk().withdraw()
        path2results = askopenfilename(filetype=(("XLSX File", "*.xlsx"), ("CSV File", "*.csv")),
                                    title="Choose a file with results of classification")
        if (path2results == ''):
            exit(0)
        if (path2results[-4:]=="xlsx"):
            results = results2dict(readXLSX(path2results))
        if (path2results[-3:]=="csv"):
            results = results2dict(readCSV(path2results))


        '''''''''''''''''
        # Reports folder window
        '''''''''''''''''
        Tk().withdraw()
        path2reports = askdirectory(title="Choose a folder which contain reports")
        if (path2reports == ''):
            exit(0)
        reportsList = [os.path.join(path2reports, f) for f in os.listdir(path2reports) if
                       os.path.isfile(os.path.join(path2reports, f))]

    '''''''''''''''''
    # Data collection
    '''''''''''''''''
    histPer, parts, files, wakefulness, stages=groupStatistic(results,reportsList)
    columns=list(results.keys())

    csv=[[]]
    for matFile in range(len(wakefulness)):
        if wakefulness[matFile][:8]!=wakefulness[matFile-1][:8]:
            csv.append([])
        csv[-1].append(wakefulness[matFile])
    if csv[0]==[]:
        csv=csv[1:]

    # write2csv(csv,"Z:\\Tetervak\\Analysed\\"+"0 in 6 group "+fileName(path2results)+".csv")
    # exit(0)


    '''''''''''''''''
    # Plotting
    '''''''''''''''''

    high, width=recSubPlotDet(len(columns)+1)

    x.rcParams.update({'font.size': 14})
    plt.figure(figsize=(40.0, 25.0))
    names = ["Artifacts", "Wakefulness", "First stage", "Second stage", "Third stage", "Fourth stage", "Fifth stage",
             "Sixth stage", "Seventh stage"]
    for column in range(len(columns)):
        #labels = [str(histPer[column][i]) for i in range(len(histPer[column]))]
        a=plt.subplot(high,width,column+1)
        plt.bar(stages,histPer[column],align='center')
        plt.title("Group "+str(column+1))
        plt.ylabel("Percentage")
        a.set_xticks([tick-0.0 for tick in stages])
        a.set_xticklabels([str(s) for s in stages])
        #plt.xticks(rotation=50)
        plt.axis([ stages[0]-0.5, 3+0.5, 0,100])
        for k in range(len(stages)):
            a.text(stages[k]-0.40, histPer[column][k] + 0.35, str(histPer[column][k]), color='blue')


    a=plt.subplot(high, width, high*width)
    plt.bar(stages,files, color='g',align='center')
    plt.title("Total number of stages")
    plt.ylabel("Percentage")
    a.set_xticks([tick - 0.0 for tick in stages])
    a.set_xticklabels([str(s) for s in stages])
    #plt.xticks(rotation=50)
    plt.axis([stages[0]-0.5, stages[-1]+0.5, 0, 100])
    for k in range(len(stages)):
        a.text(stages[k] - 0.40, files[k] + 0.35, str(files[k]), color='green')
    plt.subplots_adjust(hspace=0.3)
    plt.savefig("Z:\\Tetervak\\Analysed\\"+fileName(path2results)+"_HIST.jpg", dpi=300)



















"""
def sergey2lavrov(matName:str)->str:
    return ''.join([v+'_' for v in matName.split('_')][:3])[:-1]+".mat("+str(int(int(matName.split('_')[-2])/30))+")'"

def write2csv(some2Dlist:list, path2save:str):
    if type(some2Dlist[0])!=list:
        print("You should give a list of lists to write it for csv")
        exit(0)
    try:
        with open(path2save, 'w') as file:
            for k in range(max([len(l) for l in some2Dlist])):
                line=''
                for column in some2Dlist:
                    if k>=len(column):
                        line+=';'
                    else:
                        line+=column[k]+';'
                file.write(line[:-1]+'\n')
            file.close()
        print("Saved : "+path2save)
        return True
    except:
        return False


path2results="Z:\\Tetervak\\9_data14_3_30sec_all_20171027_172800.xlsx"
results=readXLSX(path2results)
converted=[[] for column in results]
for i, group in enumerate(results):
    for fileName in group:
        if len(fileName.split('_'))==6 or fileName=='':
            continue
        converted[i].append(sergey2lavrov(fileName))

write2csv(converted, "Z:\\Tetervak\\Test.csv")

"""