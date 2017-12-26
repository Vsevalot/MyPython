import os
import mypyfunctions as myPy
import datetime



STAGES = [-1, 0, 1, 2, 3, 4, 5, 6, 7]
STAGE_NAMES = ["Artifacts(-1)", "Wakefulness(0)", "1 stage", "2 stage", "3 stage", "4 stage", "5 stage",
         "6 stage", "7 stage"]
STAGE_NAMES = {STAGES[i]: STAGE_NAMES[i] for i in range(len(STAGES))}


class EEG_Fragment(object):  # contain name of the eeg fragment, stage and ketamine drugs
    def __init__(self, matfile_name: str, report: str = None, stage: int = None, ketamine: bool = None):
        self.stage = stage
        self.day_time = matName2Time(matfile_name)[0]
        self.ketamine = ketamine
        self.name = matfile_name
        self.report_name = report


class Record(object):  # one line in a report ( 11:37:53 | 3 | Artifacts )
    def __init__(self, report_path: str, time: str, stage: str, comment: str = None):
        self.time = myPy.reportTime(time, report_path)
        if stage in [str(s) for s in STAGES]:
            self.stage = int(stage)
        else:
            self.stage = "Unknown stage: " + stage
        self.comment = comment


class Report(object):  # a list of records, with name, date and ketamine drugs
    def chronoChecker(self):  # check that all times are in correct order
        for i in range(1, len(self.records), 1):
            if self.records[i].time < self.records[i - 1].time:
                self.correct_report = False
                first_time = str(self.records[i - 1].time.time())
                second_time = str(self.records[i].time.time())
                self.reason = "Incorrect time order: " + first_time + '->' + second_time



    def __init__(self, report_path, csv):
        self.name = myPy.fileFromPath(report_path)
        if self.name[:3] == "(k)" or self.name[:3] == "(K)":
            self.ketamine = True
            self.name = self.name[3:]
        else:
            self.ketamine = False

        if len(csv) < 2 or len(csv) > 3:
            self.correct_report = False
            self.reason = "Report should have 2 or 3 columns, got " + str(len(csv)) + " instead"
            return

        self.records = []
        for i in range(len(csv[0])):
            if len(csv) == 2:
                self.records.append(Record(report_path, csv[0][i], csv[1][i]))
            if len(csv) == 3:
                self.records.append(Record(report_path, csv[0][i], csv[1][i], csv[2][i]))

        self.correct_report = True
        self.reason = ''

        for rec in self.records:
            if type(rec.time) != datetime.datetime:
                self.correct_report = False
                self.reason = rec.time
                break
            if type(rec.stage) != int:
                self.correct_report = False
                self.reason = rec.stage
                break


        if self.correct_report:
            self.records[0].time -= datetime.timedelta(
                seconds=10)  # pick first time for 10 seconds earlier to allow 12:22:01 mat file find 12:21:59 record
            self.records[-1].time += datetime.timedelta(
                seconds=10)  # pick last time for 10 seconds later to allow 12:22:59 mat file find 12:23:01 record
            self.day_time = self.records[0].time
            self.chronoChecker()


'''
matfile_name should looks like: folder_date_time(startSec - stopSec).mat
'''
def matName2Time(matfile_name: str) -> [datetime.datetime, int]:  # convert Mat file's name to date and time
    time_delta = 300
    start_second = 0
    if '(' in matfile_name:
        time_delta = matfile_name.split('(')[1].split(')')[0]  # this will be the number of seconds since the fragment beginning
        start_second = int(time_delta.split('-')[0])  # if time delta looks like 100-120
        time_delta = int(time_delta.split('-')[1]) - int(time_delta.split('-')[0])  # time delta  = 120-100 = 20 seconds


    name = matfile_name.split('_')
    if '(' in name[-1]:
        name[-1] = name[-1].split('(')[0]

    dt = datetime.datetime(int(name[-2][0:4]), int(name[-2][4:6]), int(name[-2][6:8]), # YYYY, MM, DD
                           int(name[-1][:2]), int(name[-1][3:5]), # HH, MM, SS
                           int(name[-1][6:8])) + datetime.timedelta(seconds=start_second)
    return [dt, time_delta]



def getStage(matfile: str, reports: list):
    eeg_time, time_delta = matName2Time(matfile)
    rec = '_'.join(matfile.split('_')[:-2])
    r = [r for r in reports if ('_'.join(r.name.split('_')[:-1])==rec) and (r.records[0].time<eeg_time)
                  and (r.records[-1].time>eeg_time)]
    if len(r)>0: # if found a report with the same recXXX
        report = r[0]
        time_dif = [s.time.timestamp() - eeg_time.timestamp() for s in report.records]
        closest = time_dif.index(min([s for s in time_dif if s > 0]))
        stages = {stage: 0 for stage in STAGES}
        for i in range(closest, len(report.records), 1):
            if (eeg_time.timestamp() - report.records[i].time.timestamp() < 0):
                if i == closest:
                    stages[report.records[i - 1].stage] += report.records[i].time.timestamp() - eeg_time.timestamp()
                else:
                    stages[report.records[i - 1].stage] += report.records[i].time.timestamp() - \
                                                           report.records[i - 1].time.timestamp()
            if sum([stages[stage] for stage in stages]) > time_delta:
                stages[report.records[i - 1].stage] -= report.records[i].time.timestamp() - \
                                                       report.records[i - 1].time.timestamp()
                stages[report.records[i - 1].stage] += time_delta - sum([stages[stage] for stage in stages])
                break

        if sum([stages[stage] for stage in stages if stage!=-1])<30: # if the fragment has less than 30 seconds of non
            eeg_stage = -1                                           # artefacted stages, it's an artefacted fragment
        else:
            eeg_stage = round(sum([stages[stage]*(stage+1) for stage in stages if stage!=-1])/(time_delta-stages[-1]))-1
        if eeg_stage in [0,1,2,3]:
            return "{};{}\n".format(matfile, eeg_stage)
        else:
            return None
    else:
        return None

# path_to_files = "Z:\\Lavrov\\records30sec"
# files = [f for f in os.listdir(path_to_files) if os.path.isfile(os.path.join(path_to_files, f))]
# with open("Z:\\Tetervak\\All_files_30_sec.csv", 'w') as file:
#     for f in files:
#         file.write(f+'\n')
#     file.close()
# exit(0)


path_to_reports = "Z:\\Tetervak\\Reports\\complete"
REPORTS = [os.path.join(path_to_reports, f) for f in os.listdir(path_to_reports)
           if os.path.isfile(os.path.join(path_to_reports, f))]
REPORTS = [Report(report, myPy.readCSV(report)) for report in REPORTS]

if __name__ == "__main__":

    path_to_save = "Z:\\Tetervak\\File-stage_30_sec_new.csv"
    fragments = myPy.readCSV("Z:\\Tetervak\\All_files_30_sec.csv")[0]
    fragments = [getStage(f, REPORTS) for f in fragments]
    fragments = [f for f in fragments if f is not None]
    with open(path_to_save, 'w') as file:
        for f in fragments:
            file.write(f)

    print("complete")




