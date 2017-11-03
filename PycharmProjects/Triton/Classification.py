import os
import datetime
import matplotlib as x
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory


'''
Get datetime object from string looks like 1123 or 11:23 etc 
'''
def reportTime(string_time: str, report_path: str) -> datetime.datetime: # convert string to time in the given report
    year = int("20"+report_path[-6:-4])
    month = int (report_path[-8:-6])
    day = int (report_path[-10:-8])
    point=':' # default delimiter
    for char in string_time:
        if char=='.':
            point = '.'
            break
        if char=='-':
            point = '-'
            break
    t = string_time.split(point)
    try:
        if (len(t) == 1): # if there are no delimiters in the time
            t = t[0]
            if (len(t) == 3) or (len(t) == 4):  # if time 12:33:00 in format 1233
                return datetime.datetime(year, month, day, int(t[:-2]), int(t[-2:]), 00)
            if (len(t) == 5) or (len(t) == 6):
                return datetime.datetime(year, month, day, int(t[:-4]), int(t[-4:-2]), int(t[-2:])) # if time 12:33:00 in format 123300
            print("Something goes wrong, check time format:", report_path, ''.join(t))
            exit(1)
        if (len(t) == 2): # if there is one delimiter in the time
            if (len(t[0])==2 or len(t[0])==1) and len(t[1])==2:
                return datetime.datetime(year, month, day, int(t[0]), int(t[1]), 00)
            print("Something goes wrong, check time format:", report_path, ''.join(t))
            exit(1)
        if (len(t)==3): # if there are two delimiters in the time
            if (len(t[0])==2 or len(t[0])==1) and len(t[1])==2 and  len(t[2])==2:
                return datetime.datetime(year, month, day, int(t[0]), int(t[1]), int(t[2]))
            print("Something goes wrong, check time format:", report_path, ''.join(t))
            exit(1)
        print("Something goes wrong, check time format:", report_path, ''.join(t))
        exit(1)
    except:
        print("Something goes wrong, check time format:", report_path, ''.join(t))
        exit(1)


'''
Get name of the file from the file_path
'''
def fileFromPath(file_path:str)->str:
    for i in range(len(file_path)-1,-1,-1):
        if file_path[i]=='.':
            file_path=file_path[:i]
            break
    for i in range(len(file_path)-1,-1,-1):
        if file_path[i]=='\\':
            file_path=file_path[i+1:]
            break
    return file_path


'''
matfile_name should looks like: folder_date_time(startSec - stopSec).ext
Extension does not matter
'''
def matName2Time(matfile_name: str) -> [datetime.datetime, int]: # convert Mat file's name to date and time
    time_delta=matfile_name.split('(')[1].split(')')[0] # this will be the number of seconds since the fragment beginning
    if '-' in time_delta:
        start_second = int(time_delta.split('-')[0]) # if time delta looks like 100-120
        time_delta = int(time_delta.split('-')[1]) - int(time_delta.split('-')[0]) # time delta  = 120-100 = 20 seconds
    else:
        time_delta = 30
        start_second = time_delta*int(time_delta) # if in only 30 seconds parts

    name=matfile_name.split('_')
    dt = datetime.datetime(int(name[1][0:4]), int(name[1][4:6]), int(name[1][6:8]), int(name[2][:2]), int(name[2][3:5]),
                           int(name[2][6:8])) + datetime.timedelta(seconds=start_second)
    return [dt, time_delta]


'''
Read any csv and return list of lists with list of values for each column
'''
def readCSV(csv_path:str) -> list: # read any CSV file and return it like list of columns
    with open(csv_path, 'r') as file:
        lines=[line.split(';') for line in file.readlines()] # reading all lines in the file with rows as elements of the list
        for line in range(len(lines)):
            if lines[line][-1][-1]=='\n':
                lines[line][-1]=lines[line][-1][:-1]

        ignore = ['\t', ' ']
        for i in range(len(lines)):
            for k in range(len(lines[i])):
                if lines[i][k] in ignore:
                    lines[i][k] = ''

        empty_line=True
        while(empty_line): # remove all empty lines
            for value in lines[-1]:
                if(value != ''):
                    empty_line=False
            if(empty_line):
                del lines[-1]

        data=[[value[i] for value in lines] for i in range(len(lines[0]))] # transpose the list to make columns elements of the list
        return data


'''
Read any xlsx and return list of lists with list of values for each column
'''
def readXLSX(xlsx_path:str)->list:
    from openpyxl import load_workbook
    wb = load_workbook(filename=xlsx_path, read_only=True)
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


'''
Convert read csv list of lists to dictionary of lists
'''
def results2Dict(results:list) -> dict: # convert values from "'abc'\n" to "abc"
    for i in range(len(results)):
        for k in range(len(results[i])):
            if results[i][k]!='':
                if results[i][k][0]=="'":
                    results[i][k]=results[i][k][1:]
                if results[i][k][-1]=="'" :
                    results[i][k] = results[i][k][:-1]
                if results[i][k][0]=="\t":
                    results[i][k]=results[i][k][1:]
            else:
                results[i]=results[i][:k]
                break
    return {"Column_"+str(i+1):results[i] for i in range(len(results))}


class EEG_Fragment(object):
    def __init__(self, matfile_name:str, stage:int, ketamine: bool = None):
        self.stage = stage
        self.day_time = matName2Time(matfile_name)[0]
        self.ketamine = ketamine
        if matfile_name[:7] == "folder_":
            matfile_name = matfile_name[7:]
        self.name = matfile_name


class Record(object):
    def __init__(self, report_path:str, time:str, stage:str, comment:str=None):
        self.time = reportTime(time, report_path)
        self.stage = int(stage)
        self.comment = comment


class Report(object):
    def chronoChecker(self): # check that all times are in correct order
        for i in range(1,len(self.records),1):
            if self.records[i].time < self.records[i-1].time:
                print("Wrong time order check file:", self.name, str(self.records[i].time))
                exit(0)
        return True


    def __init__(self, report_path, csv):
        self.name = fileFromPath(report_path)
        if self.name[:3]=="(k)" or self.name[:3]== "(K)":
            self.ketamine=True
        else:
            self.ketamine=False

        self.records = []
        for i in range(len(csv[0])):
            if len(csv)==2:
                self.records.append(Record(report_path,csv[0][i],csv[1][i]))
            if len(csv)==3:
                self.records.append(Record(report_path,csv[0][i],csv[1][i], csv[2][i]))
        self.records[0].time-=datetime.timedelta(seconds=30) # pick first time for 30 seconds earlier to allow 12:22:01 mat file find 12:21:59 record
        self.day_time = self.records[0].time
        self.chronoChecker()


STAGES = [-1, 0, 1, 2, 3, 4, 5, 6, 7]

def getStage(matfile:str, reports:list):
    eeg_time, time_delta = matName2Time(matfile)
    day_reports = [report for report in reports if (report.day_time.year == eeg_time.year) and
                   (report.day_time.month == eeg_time.month) and (report.day_time.day == eeg_time.day)]

    for report in day_reports:
        if (report.records[0].time>eeg_time) or (report.records[-1].time<eeg_time):
            continue

        for i in range(len(report.records)):
            record_time = report.records[i].time
            record_stage = report.records[i].stage
            if record_time >= eeg_time:  # if found a record which time is later or equal than matfile's time
                stages = {stage: 0 for stage in STAGES}
                stages[record_stage] += (record_time - eeg_time).seconds
                k = i + 1
                if (k == len(report.records)):
                    return EEG_Fragment(matfile, record_stage, report.ketamine)
                while ((report.records[k].time - eeg_time).seconds < time_delta):
                    stages[report.records[k].stage] += (report.records[k].time - report.records[k - 1].time).seconds
                    k += 1
                    if k == len(report.records):
                        k -= 1
                        break
                if sum([stages[stage] for stage in stages]) < time_delta:
                    stages[report.records[k].stage] += time_delta - (report.records[k - 1].time - eeg_time).seconds
                eeg_stage = max(stages, key=stages.get)
                return EEG_Fragment(matfile, eeg_stage, report.ketamine)

        return None


def matFiles2eegFragments(results: dict, reports_list: list):
    reports = [Report(report, readCSV(report)) for report in reports_list]
    group_names = list(results.keys())
    for group in group_names:
        for matfile in range(len(results[group])):
            results[group][matfile]=getStage("folder_"+results[group][matfile], reports)
    return results

if __name__ == "__main__":
    '''''''''''''''''
    # Preparing files
    '''''''''''''''''
    results=''
    path2results = "Z:\\Tetervak\\21_data14_4_30sec_20171031_171400.csv"
    if (path2results[-4:] == "xlsx"):
        results = results2Dict(readXLSX(path2results))
    if (path2results[-3:] == "csv"):
        results = results2Dict(readCSV(path2results))
    path2reports = "E:\\test\\Reports\\complete"
    reports_list = [os.path.join(path2reports, f) for f in os.listdir(path2reports) if
                    os.path.isfile(os.path.join(path2reports, f))]
    try:
        path2results = "Z:\\Tetervak\\21_data14_4_30sec_20171031_171400.csv"
        if (path2results[-4:]=="xlsx"):
            results = results2Dict(readXLSX(path2results))
        if (path2results[-3:]=="csv"):
            results = results2Dict(readCSV(path2results))
        path2reports = "E:\\test\\Reports\\complete"
        reports_list = [os.path.join(path2reports, f) for f in os.listdir(path2reports) if
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
            results = results2Dict(readXLSX(path2results))
        if (path2results[-3:]=="csv"):
            results = results2Dict(readCSV(path2results))


        '''''''''''''''''
        # Reports folder window
        '''''''''''''''''
        Tk().withdraw()
        path2reports = askdirectory(title="Choose a folder which contain reports")
        if (path2reports == ''):
            exit(0)
        reports_list = [os.path.join(path2reports, f) for f in os.listdir(path2reports) if
                       os.path.isfile(os.path.join(path2reports, f))]

    eeg_fragments=matFiles2eegFragments(results,reports_list)
    processed_records = sum([eeg_fragments[g].count(None) for g in eeg_fragments]) / \
                        sum([len(eeg_fragments[g]) for g in eeg_fragments])

    print(processed_records)


