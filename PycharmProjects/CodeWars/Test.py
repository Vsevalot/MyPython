import datetime

'''
    Get datetime object from string looks like 1123 or 11:23 etc 
'''
def reportTime(string_time: str, report_path: str): # convert string to time in the given report
    point=':' # default delimiter
    for char in string_time:
        if char=='.':
            point = string_time.split('.')
            break
        if char=='-':
            point = string_time.split('-')
            break
    t = string_time.split(point)
    try:
        if (len(t) == 1): # if there are no delimiters in the time
            t = t[0]
            if (len(t) == 3) or (len(t) == 4):  # if time 12:33:00 in format 1233
                return datetime.datetime(0,0,0,int(t[:-2]), int(t[-2:]), 00)
            if (len(t) == 5) or (len(t) == 6):
                return datetime.datetime(0,0,0,int(t[:-4]), int(t[-4:-2]), int(t[-2:])) # if time 12:33:00 in format 123300
            print("Something goes wrong, check time format:", report_path)
            exit(1)
        if (len(t) == 2): # if there is one delimiter in the time
            if (len(t[0])==2 or len(t[0])==1) and len(t[1])==2:
                return datetime.datetime(0,0,0,int(t[0]), int(t[1]), 00)
            print("Something goes wrong, check time format:", report_path)
            exit(1)
        if (len(t)==3): # if there are two delimiters in the time
            if (len(t[0])==2 or len(t[0])==1) and len(t[1])==2 and  len(t[2])==2:
                return datetime.datetime(0,0,0,int(t[0]), int(t[1]), int(t[2]))
            print("Something goes wrong, check time format:", report_path)
            exit(1)
        print("Something goes wrong, check time format:", report_path)
        exit(1)
    except:
        print("Something goes wrong, check time format:", report_path)
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
def matName2Time(matfile_name: str): # convert Mat file's name to date and time
    time_delta=matfile_name.split('(')[1].split(')')[0] # this will be the number of seconds since the fragment beginning
    if '-' in time_delta:
        time_delta = int(time_delta.split('-')[0]) # if time delta looks like 100-120
    else:
        time_delta = 30*int(time_delta) # if in only 30 seconds parts

    name=matfile_name.split('_')
    dt = datetime.datetime(int(name[1][0:4]), int(name[1][4:6]), int(name[1][6:8]), int(name[2][:2]), int(name[2][3:5]),
                           int(name[2][6:8])) + datetime.timedelta(seconds=time_delta)
    return dt


class EegFragment(object):
    def __init__(self, matfile_name:str, stage:str):
        self.name = matfile_name
        self.stage = stage
        self.day_time = matName2Time(matfile_name)
        if matfile_name[:3]=="(k)" or matfile_name[:3]== "(K)":
            self.ketamine=True
        else:
            self.ketamine=False


class Record(object):
    def __init__(self, report_path, time, stage, comment=None):
        self.time = reportTime(time, report_path)
        self.stage = int(stage)
        self.comment = comment

    def __add__(self, sec): # adding seconds to the record's time
        return self.time + datetime.timedelta(seconds=sec)

    def __sub__(self, sec): # adding seconds to the record's time
        return self.time - datetime.timedelta(seconds=sec)


class Report(object):
    def __init__(self, report_path, csv):
        self.name = fileFromPath(report_path)
        self.records = []
        for i in range(len(csv)):
            if len(csv)==2:
                self.records.append(Record(report_path,csv[0][i],csv[1][i]))
            if len(csv)==3:
                self.records.append(Record(report_path,csv[0][i],csv[1][i], csv[2][i]))

    def chronoChecker(self): # check that all times are in correct order
        for i in range(1,len(self.records)):
            if self.records[i] < self.records[i-1]:
                print("Wrong time order check file:", self.name, str(self.records[i]))
                exit(0)
            return True
        return False


if __name__ == "__main__":
    '''''''''''''''''
    # Preparing files
    '''''''''''''''''
    try:
        path2results = "Z:\\Tetervak\\21_data14_4_30sec_20171031_171400.csv"
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

