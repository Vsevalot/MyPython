import os
import datetime
import matplotlib
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showwarning

def errMsg(message: str, code: int = 1):
    showerror("Error", message)
    exit(code)


def warningMsg(warnings_list: list):
    warnings='\n'.join(warnings_list)
    msg = "During operation, the following errors occurred:\n\n" + warnings
    msg += "\n\nThese reports were not used in the statistic."
    showwarning("Warning", msg)



'''
Gets datetime object from a string looks like 1123 or 11:23 etc 
'''
def reportTime(string_time: str, report_path: str):  # convert string to time in the given report
    year = int("20" + report_path[-6:-4])
    month = int(report_path[-8:-6])
    day = int(report_path[-10:-8])
    point = ':'  # default delimiter
    for char in string_time:
        if char == '.':
            point = '.'
            break
        if char == '-':
            point = '-'
            break
        if char == '\\':
            point = '\\'
            break
        if char == '/':
            point = '/'
            break
    t = string_time.split(point)

    if (len(t) == 1):  # if there are no delimiters in the time
        t = t[0]
        if (len(t) == 3) or (len(t) == 4):  # if time 12:33:00 in format 1233
            return datetime.datetime(year, month, day, int(t[:-2]), int(t[-2:]), 00)
        if (len(t) == 5) or (len(t) == 6):
            return datetime.datetime(year, month, day, int(t[:-4]), int(t[-4:-2]),
                                     int(t[-2:]))  # if time 12:33:00 in format 123300
        return "Something goes wrong, check time format of: " + report_path + ' ' + ''.join(t)
    if (len(t) == 2):  # if there is one delimiter in the time
        if (len(t[0]) == 2 or len(t[0]) == 1) and len(t[1]) == 2:
            return datetime.datetime(year, month, day, int(t[0]), int(t[1]), 00)
        return "Something goes wrong, check time format of: " + report_path + ' ' + ''.join(t)
    if (len(t) == 3):  # if there are two delimiters in the time
        if (len(t[0]) == 2 or len(t[0]) == 1) and len(t[1]) == 2 and len(t[2]) == 2:
            return datetime.datetime(year, month, day, int(t[0]), int(t[1]), int(t[2]))
        return "Something goes wrong, check time format of: " + report_path + ' ' + ''.join(t)
    return "Something goes wrong, check time format of: " + report_path + ' ' + ''.join(t)


'''
Gets a name of a file from the file_path
'''
def fileFromPath(file_path: str) -> str:
    if '\\' in file_path:
        file_name = ''.join(file_path.split('\\')[-1])
    elif '/' in file_path:
        file_name = ''.join(file_path.split('/')[-1])
    else:
        print("Incorrect file path: ", file_path)
        exit(1)
    for i in range(len(file_name) - 1, -1, -1):  # remove expansion from file name
        if file_name[i] == '.':
            return file_name[:i]
    return file_name


'''
matfile_name should looks like: folder_date_time(startSec - stopSec).mat
'''
def matName2Time(matfile_name: str) -> [datetime.datetime, int]:  # convert Mat file's name to date and time
    time_delta = matfile_name.split('(')[1].split(')')[
        0]  # this will be the number of seconds since the fragment beginning
    if '-' in time_delta:
        start_second = int(time_delta.split('-')[0])  # if time delta looks like 100-120
        time_delta = int(time_delta.split('-')[1]) - int(time_delta.split('-')[0])  # time delta  = 120-100 = 20 seconds
    else:
        start_second = 30 * int(time_delta)  # if in only 30 seconds parts
        time_delta = 300

    name = matfile_name.split('_')
    if (len(name)==2):
        name.insert(0, "folder")
    dt = datetime.datetime(int(name[1][0:4]), int(name[1][4:6]), int(name[1][6:8]), int(name[2][:2]), int(name[2][3:5]),
                           int(name[2][6:8])) + datetime.timedelta(seconds=start_second)
    return [dt, time_delta]


'''
Reads any csv and returns a list of lists with list of values for each column
'''
def readCSV(csv_path: str) -> list:  # read any CSV file and return it like list of columns
    with open(csv_path, 'r') as file:
        lines = [line.split(';') for line in
                 file.readlines()]  # reading all lines in the file with rows as elements of the list
        for line in range(len(lines)):
            if lines[line][-1][-1] == '\n':
                lines[line][-1] = lines[line][-1][:-1]

        ignore = ['\t', ' ']
        for i in range(len(lines)):
            for k in range(len(lines[i])):
                if lines[i][k] in ignore:
                    lines[i][k] = ''

        empty_line = True
        while (empty_line):  # remove all empty lines
            for value in lines[-1]:
                if (value != ''):
                    empty_line = False
            if (empty_line):
                del lines[-1]

        data = [[value[i] for value in lines] for i in
                range(len(lines[0]))]  # transpose the list to make columns elements of the list
        return data


'''
Reads any xlsx and returns list of lists with list of values for each column
'''
def readXLSX(xlsx_path: str) -> list:
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
Converts csv list of lists to dictionary of lists
'''
def results2Dict(results: list) -> dict:  # convert values from "'abc'\n" to "abc"
    for i in range(len(results)):
        for k in range(len(results[i])):
            if results[i][k] != '':
                if results[i][k][0] == "'":
                    results[i][k] = results[i][k][1:]
                if results[i][k][-1] == "'":
                    results[i][k] = results[i][k][:-1]
                if results[i][k][0] == "\t":
                    results[i][k] = results[i][k][1:]
            else:
                results[i] = results[i][:k]
                break
    return {"Group " + str(i + 1): results[i] for i in range(len(results))}


class EEG_Fragment(object):  # contain name of the eeg fragment, stage and ketamine drugs
    def __init__(self, matfile_name: str, report: str = None, stage: int = None, ketamine: bool = None):
        self.stage = stage
        self.day_time = matName2Time(matfile_name)[0]
        self.ketamine = ketamine
        self.name = matfile_name
        self.report_name = report


class Record(object):  # one line in a report ( 11:37:53 | 3 | Artifacts )
    def __init__(self, report_path: str, time: str, stage: str, comment: str = None):
        self.time = reportTime(time, report_path)
        self.stage = int(stage)
        self.comment = comment


class Report(object):  # a list of records, with name, date and ketamine drugs
    def chronoChecker(self):  # check that all times are in correct order
        for i in range(1, len(self.records), 1):
            if self.records[i].time < self.records[i - 1].time:
                self.correct_report = False
                self.reason = "Incorrect time order: " + str(self.records[i].time) + '->' + str(self.records[i - 1].time)


    def __init__(self, report_path, csv):
        self.name = fileFromPath(report_path)
        if self.name[:3] == "(k)" or self.name[:3] == "(K)":
            self.ketamine = True
        else:
            self.ketamine = False

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


        if self.correct_report:
            self.records[0].time -= datetime.timedelta(
                seconds=10)  # pick first time for 10 seconds earlier to allow 12:22:01 mat file find 12:21:59 record
            self.records[-1].time += datetime.timedelta(
                seconds=10)  # pick last time for 10 seconds later to allow 12:22:59 mat file find 12:23:01 record
        self.day_time = self.records[0].time
        self.chronoChecker()


STAGES = [-1, 0, 1, 2, 3, 4, 5, 6, 7]
STAGE_NAMES = ["Artifacts", "Wakefulness", "First stage", "Second stage", "Third stage", "Fourth stage", "Fifth stage",
         "Sixth stage", "Seventh stage"]

'''
Finds stage for the matfile in the reports. If not found returns EEG_Fragment with None stage
'''
def getStage(matfile: str, reports: list):
    eeg_time, time_delta = matName2Time(matfile)
    day_reports = [report for report in reports if (report.day_time.year == eeg_time.year) and
                   (report.day_time.month == eeg_time.month) and (report.day_time.day == eeg_time.day)]

    for report in day_reports:
        if (report.records[0].time > eeg_time) or (report.records[-1].time < eeg_time):
            continue

        time_dif = [abs((eeg_time.timestamp() - s.time.timestamp())) for s in report.records ]
        closest = time_dif.index(min(time_dif))
        stages = {stage: 0 for stage in STAGES}
        i = closest
        while (1):
            stages[report.records[i].stage] += abs((eeg_time - report.records[i].time).seconds)
            i+=1
            if i == len(report.records):
                if sum([stages[stage] for stage in stages]) > time_delta:
                    stages[report.records[i-1].stage]-= abs((eeg_time - report.records[i-1].time).seconds)
                    stages[report.records[i - 1].stage] += time_delta - sum([stages[stage] for stage in stages])
                eeg_stage = max(stages, key=stages.get)
                return EEG_Fragment(matfile, report.name, eeg_stage, report.ketamine)
            if sum([stages[stage] for stage in stages]) > time_delta:
                stages[report.records[i - 1].stage] -= abs((eeg_time - report.records[i - 1].time).seconds)
                stages[report.records[i - 1].stage] += time_delta - sum([stages[stage] for stage in stages])
                eeg_stage = max(stages, key=stages.get)
                return EEG_Fragment(matfile, report.name, eeg_stage, report.ketamine)
    return EEG_Fragment(matfile)


'''
Takes a dictionary of matfiles lists and returns dictionary of EEG_Fragments
'''
def matfiles2eegFragments(results: dict, reports_list: list):
    reports = [Report(report, readCSV(report)) for report in reports_list]
    correct_reports = [r for r in reports  if r.correct_report == True]
    incorrect_reports = [r for r in reports if r.correct_report == False]
    group_names = list(results.keys())
    for group in group_names:
        for matfile in range(len(results[group])):
            results[group][matfile] = getStage("folder_" + results[group][matfile], correct_reports)

    if incorrect_reports!=[]:
        err_msgs=["File: " + report.name + ", reason: " + report.reason for report in incorrect_reports ]
        warningMsg(err_msgs)
    return results


'''
Writes a list of lists to csv
'''
def write2csv(twoD_list: list, file_name: str, path2save: str = ''):
    if type(twoD_list[0]) != list:
        print("You should give a list of lists to write it for csv")
        exit(0)
    try:
        if path2save != '':
            path2save += '\\'  # to make full path to file from path and file name
        with open(path2save + file_name + '.csv', 'w') as file:
            for k in range(max([len(l) for l in twoD_list])):
                line = ''
                for column in twoD_list:
                    if k >= len(column):
                        line += ';'
                    else:
                        line += column[k] + ';'
                file.write(line[:-1] + '\n')
            file.close()
        return True
    except:
        return False


'''
Takes a dictionary of stages for groups which files should be write to csv and save them to the result's folder
'''
def writeCSVforInterestedFiles(file_dict: dict, eeg: dict, save_path: str):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for group in file_dict:
        if file_dict[group] == []:
            continue
        for stage in file_dict[group]:
            csv = [eeg_fragment for eeg_fragment in eeg[group] if eeg_fragment.stage == stage]
            if csv == []:
                continue

            reports = []  # names of all reports used for the fragments in the csv
            for fragments in csv:
                if fragments.report_name not in reports:
                    reports.append(fragments.report_name)

            csv = [ ["Report : " + report_name] + [eeg_fragment.name for eeg_fragment in csv
                   if eeg_fragment.report_name == report_name] for report_name in reports]
            try:
                write2csv(csv, group + '_stage_' + str(stage), save_path)
            except:
                write2csv(csv, group + '_stage_' + str(stage))


'''
Calculates number of rows (high) and number of columns (width) of subplot for the best screen ratio 
'''
def recSubPlotDet(plotNumber: int):
    n = plotNumber
    factors = []
    i = 2
    while (n != 1):  # feed factors arr with factors 18 = [2,3,3]
        if n % i == 0:
            factors.append(i)
            n /= i
        else:
            i += 1

    if len(factors) == 1:  # we need a rectangular subplot, so 3*1 is not enough -> 2*2
        return recSubPlotDet(plotNumber + 1)
    if len(factors) > 2:
        i = 0
        while (len(factors) != 2):
            factors[i % 2] *= factors[-1]
            i += 1
            factors.pop(-1)
    if (factors[1] < factors[0]):  # if width < high swap them
        return factors[1], factors[0]
    return factors[0], factors[1]


'''
Plots histograms for each non empty group and save them to the result's folder
'''
def subPlotter(eeg: dict, stage_ignore: list, save_path: str):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    local_stages = [stage for stage in STAGES if stage not in stage_ignore]

    sum_of_fragments = sum([len([fragment for fragment in eeg[group] if (fragment.stage is not None) and
                                 (fragment.stage not in stage_ignore)]) for group in eeg])

    bar_values = {group: {stage: len([fragment.stage for fragment in eeg[group] if fragment.stage == stage])
                          for stage in local_stages} for group in eeg}

    for group in bar_values:
        if all(bar_values[group][stage] == 0 for stage in bar_values[group]):
            bar_values[group]=None
    bar_values={group:bar_values[group] for group in bar_values if bar_values[group] is not None}

    bar_per = {group: [round(100*bar_values[group][n]/sum_of_fragments, 2) for n in bar_values[group]]
               for group in bar_values if bar_values[group]!={s: 0 for s in local_stages}}

    all_stages = [round(100*sum([bar_values[group][stage] for group in bar_values])/sum_of_fragments,2)
                  for stage in local_stages]

    # for group in bar_values:
    #     bar_values[group]={stage:bar_values[group][stage] for stage in bar_values[group].keys()
    #                        if int(stage) not in [-1,4,5,6,7]}


    group_errs={}
    for group in bar_values:
        group_errs[group]=0
        for stage in bar_values[group]:
            mult = abs(max(bar_values[group], key=bar_values[group].get)-int(stage))
            stage_val = bar_values[group][stage]
            stage_sum = sum([bar_values[group][v] for v in bar_values[group]])
            group_errs[group] += mult*stage_val/stage_sum
            pass
        group_errs[group]=round(group_errs[group],4)
    total_err = sum([group_errs[g] for g in group_errs])
    worst_group = max(group_errs, key=group_errs.get)


    '''
    Plotting
    '''
    high, width=recSubPlotDet(len(bar_values)+1)

    matplotlib.rcParams.update({"font.size": 18})
    plt.figure(figsize=(40.0, 25.0))
    i=1
    for group in bar_per:
        sbplt=plt.subplot(high,width,i)
        plt.bar(local_stages,bar_per[group],align="center")
        title = group + " ; error = " + str (group_errs[group])
        plt.title(title)
        plt.ylabel("Percentage")
        sbplt.set_xticks([tick-0.0 for tick in local_stages])
        sbplt.set_xticklabels([str(s) for s in local_stages])
        plt.axis([ local_stages[0]-0.5,  local_stages[-1]+0.5, 0,100])
        for k in range(len(local_stages)):
            sbplt.text(local_stages[k]-0.40, bar_per[group][k] + 0.35, str(bar_per[group][k]), color="blue")
        i+=1

    sbplt=plt.subplot(high, width, high*width)
    plt.bar(local_stages,all_stages, color='g',align="center")
    err_text = "Total error = " + str(total_err) +  ", the worst group - " + worst_group
    plt.text(-1,110, err_text)
    plt.title("Total stages ratio")
    plt.ylabel("Percentage")
    sbplt.set_xticks([tick - 0.0 for tick in local_stages])
    sbplt.set_xticklabels([str(s) for s in local_stages])
    plt.axis([local_stages[0] - 0.5, local_stages[-1] + 0.5, 0, 100])
    for k in range(len(local_stages)):
        sbplt.text(local_stages[k] - 0.40, all_stages[k] + 0.35, str(all_stages[k]), color='g')
    plt.subplots_adjust(hspace=0.3)
    plt.savefig(save_path+"\\HIST.jpg", dpi=300)



if __name__ == "__main__":
    '''''''''''''''''
    # Preparing files
    '''''''''''''''''
    root = Tk()
    root.withdraw()
    try:
        path2results = "Z:\\Tetervak\\21_data14_6_5min_20171108_155100.csv"
        if (path2results[-4:] == "xlsx"):
            results = results2Dict(readXLSX(path2results))
            folder_path = path2results[:-5]
        if (path2results[-3:] == "csv"):
            results = results2Dict(readCSV(path2results))
            folder_path = path2results[:-4]
        path2reports = "E:\\test\\Reports\\complete"
        reports_list = [os.path.join(path2reports, f) for f in os.listdir(path2reports) if
                        os.path.isfile(os.path.join(path2reports, f))]
    except FileNotFoundError:
        '''''''''''''''''
        # Results file window
        '''''''''''''''''
        path2results = askopenfilename(filetype=(("XLSX File", "*.xlsx"), ("CSV File", "*.csv")),
                                       title="Choose a file with results of classification")
        if (path2results == ''):
            exit(0)
        if (path2results[-4:] == "xlsx"):
            results = results2Dict(readXLSX(path2results))
            folder_path = path2results[:-5]
        if (path2results[-3:] == "csv"):
            results = results2Dict(readCSV(path2results))
            folder_path = path2results[:-4]

        '''''''''''''''''
        # Reports folder window
        '''''''''''''''''
        path2reports = askdirectory(title="Choose a folder which contain reports")
        if (path2reports == ''):
            exit(0)
        reports_list = [os.path.join(path2reports, f) for f in os.listdir(path2reports) if
                        os.path.isfile(os.path.join(path2reports, f))]


    eeg_fragments = matfiles2eegFragments(results, reports_list)  # returns the dictionary of eeg objects

    # percentage of processed records for the each group
    processed_records = [(len(eeg_fragments[g]) - len([eeg for eeg in eeg_fragments[g] if eeg.stage == None])) /
                         len(eeg_fragments[g]) if len(eeg_fragments[g]) != 0 else -1 for g in eeg_fragments]

    interested_files = {g: [] for g in eeg_fragments.keys()}
    writeCSVforInterestedFiles(interested_files, eeg_fragments, folder_path)

    subPlotter(eeg_fragments, [-1,4,5,6,7],folder_path)


