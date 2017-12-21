import os
import datetime
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Frame, LEFT, RIGHT, W, Checkbutton, Message, Button, BooleanVar, Canvas, PhotoImage, E
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showwarning
import copy


STAGES = [-1, 0, 1, 2, 3, 4, 5, 6, 7]
STAGE_NAMES = ["Artifacts(-1)", "Wakefulness(0)", "1 stage", "2 stage", "3 stage", "4 stage", "5 stage",
         "6 stage", "7 stage"]
STAGE_NAMES = {STAGES[i]: STAGE_NAMES[i] for i in range(len(STAGES))}

BAR_COLOR = "#608edb"
KETAMINE_COLOR = "#e54e37"


def pathFromName(path:str):
    delimiter = "\\"
    if '/' in path:
        delimiter='/'
    return '/'.join(path.split(delimiter)[:-1])


def errMsg(message: str, code: int = 1):
    root = Tk()
    root.withdraw()
    showerror("Error", message)
    root.destroy()
    exit(code)


def warningMsg(warnings_list: list):
    root = Tk()
    root.withdraw()
    warnings='\n'.join(warnings_list)
    msg = "During operation, the following errors occurred:\n\n{}\n\n" \
          "These reports were not used in the statistic.".format(warnings)
    showwarning("Warning", msg)
    root.destroy()

'''
Gets a name of a file from the file_path
'''
def fileFromPath(file_path: str) -> str:
    if '\\' in file_path:
        file_name = ''.join(file_path.split('\\')[-1])
    elif '/' in file_path:
        file_name = ''.join(file_path.split('/')[-1])
    else:
        errMsg(file_path)
        exit(1)
    for i in range(len(file_name) - 1, -1, -1):  # remove expansion from file name
        if file_name[i] == '.':
            return file_name[:i]
    return file_name


'''
Determines path where to save all files
'''
def savePathDeterminer(results_path):
    if '\\' in results_path:
        if (fileFromPath(results_path) != results_path.split('\\')[-2]):
            return '.'.join(results_path.split('.')[:-1])
        return '\\'.join(results_path.split('\\')[:-1])
    if (fileFromPath(results_path) != results_path.split('/')[-2]):
        return '.'.join(results_path.split('.')[:-1])
    return '/'.join(results_path.split('/')[:-1])


'''
Reads results
'''
def resultReader(results_path: str):
    try:
        return results2Dict(readXLSX(results_path)) if results_path[-4:] == "xlsx" else\
            results2Dict(readCSV(results_path)),  savePathDeterminer(results_path)
    except FileNotFoundError:
        '''''''''''''''''
        # Results file window
        '''''''''''''''''
        root = Tk()
        root.withdraw()
        path = askopenfilename(filetype=(("CSV File", "*.csv"), ("XLSX File", "*.xlsx")),
                                       title="Choose a file with results of classification")
        root.destroy()
        if (path == ''):
            exit(0)
        return results2Dict(readXLSX(path)) if path[-4:] == "xlsx" else  results2Dict(readCSV(path)),\
               savePathDeterminer(path)


'''
Prepare reports
'''
def reportReader(reports_path: str ):
    try:
        reports_list = [os.path.join(reports_path, f) for f in os.listdir(reports_path) if
                        os.path.isfile(os.path.join(reports_path, f))]
        return reports_list
    except FileNotFoundError:
        '''''''''''''''''
        # Reports folder window
        '''''''''''''''''
        root = Tk()
        root.withdraw()
        path = askdirectory(title="Choose a folder which contain reports")
        root.destroy()
        if (path == ''):
            exit(0)
        return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


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
        return ' '.join(["Wrong time format", ''.join(t)])
    if (len(t) == 2):  # if there is one delimiter in the time
        if (len(t[0]) == 2 or len(t[0]) == 1) and len(t[1]) == 2:
            return datetime.datetime(year, month, day, int(t[0]), int(t[1]), 00)
        return ' '.join(["Wrong time format", ''.join(t)])
    if (len(t) == 3):  # if there are two delimiters in the time
        if (len(t[0]) == 2 or len(t[0]) == 1) and len(t[1]) == 2 and len(t[2]) == 2:
            return datetime.datetime(year, month, day, int(t[0]), int(t[1]), int(t[2]))
        return ' '.join(["Wrong time format", ''.join(t)])
    return ' '.join(["Wrong time format", ''.join(t)])



'''
matfile_name should looks like: folder_date_time(startSec - stopSec).mat
'''
def matName2Time(matfile_name: str) -> [datetime.datetime, int]:  # convert Mat file's name to date and time
    time_delta = 300
    if '(' in matfile_name:
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

        if lines==[]:
            return []
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
    time_interval=True
    five_minutes=True
    for i in range(len(results)):
        for k in range(len(results[i])):
            results[i][k] = results[i][k].replace("'", '')
            results[i][k] = results[i][k].replace("\t", '')
            if results[i][k] != '':
                time = results[i][k].split('(')[-1].split(')')[0]
                if len(time.split('-')) == 1:
                    time_interval = False
                    if time != '0':
                        five_minutes = False
            else:
                results[i] = results[i][:k]
                break

    if time_interval:
        return {"Group " + str(i + 1): results[i] for i in range(len(results))}

    if five_minutes:
        for i in range(len(results)):
            for k in range(len(results[i])):
                results[i][k] = results[i][k].split('(')[0] + "(0-300)" + results[i][k].split('(')[-1].split(')')[-1]
        return {"Group " + str(i + 1): results[i] for i in range(len(results))}

    for i in range(len(results)):
        for k in range(len(results[i])):
            multiplier=int(results[i][k].split('(')[-1].split(')')[0])
            start = str(multiplier*30)
            finish = str((multiplier+1)*30)
            results[i][k] = results[i][k].split('(')[0] + '(' + start + '-' + finish + ')'\
                            + results[i][k].split('(')[-1].split(')')[-1]
    return {"Group " + str(i + 1): results[i] for i in range(len(results))}



class EEG_Fragment(object):  # contain name of the eeg fragment, stage and ketamine drugs
    def __init__(self, matfile_name: str, report: str = None, stage: int = None, ketamine: bool = False):
        self.stage = stage
        self.day_time = matName2Time(matfile_name)[0]
        self.ketamine = ketamine
        self.name = matfile_name
        self.report_name = report


class Record(object):  # one line in a report ( 11:37:53 | 3 | Artifacts )
    def __init__(self, report_path: str, time: str, stage: str, comment: str = None):
        self.time = reportTime(time, report_path)
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
        self.name = fileFromPath(report_path)
        if self.name[:3] == "(k)" or self.name[:3] == "(K)":
            self.ketamine = True
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


class CheckBoxes(tk.Frame):
    def __init__(self, parent, check_dict):
        tk.Frame.__init__(self, parent)
        self.boxes = {}
        i = 0
        for box in check_dict:
            self.boxes[box] = ttk.Checkbutton(self, text=str(box))
            self.boxes[box].state(['!alternate'])
            self.boxes[box].grid(row=0, column=i)
            if (check_dict[box] == True):
                self.boxes[box].state(['selected'])
            i += 1

    def state(self):
        return {box: self.boxes[box].instate(['selected']) for box in self.boxes}

    def reset(self):
        for box in self.boxes:
            self.boxes[box].state(["!selected"])


class LogsCheckBoxes(tk.Frame):
    def __init__(self, parent, check_dict):
        tk.Frame.__init__(self, parent)
        self.boxes = {}
        i = 0
        for box in check_dict:
            self.boxes[box] = ttk.Checkbutton(self, text=str(box))
            self.boxes[box].state(['!alternate'])
            self.boxes[box].grid(row=0, column=i)
            if (check_dict[box] == True):
                self.boxes[box].state(['selected'])
            i += 1

    def state(self):
        return {box: self.boxes[box].instate(['selected']) for box in self.boxes}

    def reset(self):
        for box in self.boxes:
            self.boxes[box].state(["!selected"])


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

        time_dif = [s.time.timestamp()-eeg_time.timestamp() for s in report.records ]
        closest = time_dif.index(min([s for s in time_dif if s>0]))
        stages = {stage: 0 for stage in STAGES}
        for i in range(closest, len(report.records),1):
            if (eeg_time.timestamp() - report.records[i].time.timestamp()<0):
                if i==closest:
                    stages[report.records[i-1].stage] += report.records[i].time.timestamp() - eeg_time.timestamp()
                else:
                    stages[report.records[i - 1].stage] += report.records[i].time.timestamp() - \
                                                       report.records[i-1].time.timestamp()
            if sum([stages[stage] for stage in stages]) > time_delta:
                stages[report.records[i - 1].stage] -= report.records[i].time.timestamp() - \
                                                       report.records[i-1].time.timestamp()
                stages[report.records[i - 1].stage] += time_delta - sum([stages[stage] for stage in stages])
                break
        eeg_stage = max(stages, key=stages.get)
        return EEG_Fragment(matfile, report.name, eeg_stage, report.ketamine)
    return EEG_Fragment(matfile)


'''
Takes a dictionary of matfiles lists and returns dictionary of EEG_Fragments
'''
def matfiles2eegFragments(results: dict, reports_list: list):
    eeg_fragments = copy.deepcopy(results)
    correct_reports = [r for r in reports_list  if r.correct_report == True]
    incorrect_reports = [r for r in reports_list if r.correct_report == False]
    group_names = list(results.keys())
    for group in group_names:
        for matfile in range(len(results[group])):
            if eeg_fragments[group][matfile][:3]!="rec":
                eeg_fragments[group][matfile] = getStage("folder_" + results[group][matfile], correct_reports)
            else:
                eeg_fragments[group][matfile] = getStage(results[group][matfile], correct_reports)

    if incorrect_reports!=[]:
        err_msgs=["File: " + report.name + ", reason: " + report.reason for report in incorrect_reports ]
        warningMsg(err_msgs)
    return eeg_fragments


'''
Writes a list of lists to csv
'''
def write2csv(twoD_list: list, file_name: str, path2save: str = ''):
    if type(twoD_list[0]) != list:
        errMsg("You should give a list of lists to write it for csv")
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
def writeLogs(log_dict: dict, eeg: dict, save_path: str, ketamine = False):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for group in log_dict:
        for stage in log_dict[group]:
            if log_dict[group][stage]:
                if ketamine:
                    csv = [eeg_fragment for eeg_fragment in eeg[group] if eeg_fragment.stage == stage
                           and eeg_fragment.ketamine == True]
                else:
                    csv = [eeg_fragment for eeg_fragment in eeg[group] if eeg_fragment.stage == stage]
                if csv == []:
                    continue

                reports = []  # names of all reports used for the fragments in the csv
                for fragments in csv:
                    if fragments.report_name not in reports:
                        reports.append(fragments.report_name)

                csv = [ ["Report : " + report_name] + [eeg_fragment.name for eeg_fragment in csv
                       if eeg_fragment.report_name == report_name] for report_name in reports]

                csv_name = "{} {} {}".format(group,"stage",stage)
                if ketamine:
                    csv_name = "{} ketamine".format(csv_name)
                write2csv(csv, csv_name, save_path)




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


COLORS = {}

def eegStat(eeg_fragments: dict):
    stages_stat = {}
    ketamines_stat = {}
    for group in eeg_fragments:
        stages_stat[group] = {stage:0 for stage in STAGES}
        stages_stat[group][None] = 0 # fragments without report
        ketamines_stat[group] = {stage: 0 for stage in STAGES}
        for eeg_fragment in eeg_fragments[group]:
            stages_stat[group][eeg_fragment.stage]+=1
            if eeg_fragment.ketamine == True and eeg_fragment.stage in [1,2,3]:
                ketamines_stat[group][eeg_fragment.stage] += 1

        empty_group = True
        for stage in STAGES:
            if stages_stat[group][stage] != 0:
                empty_group = False
                stages_stat[group].pop(None, None)
                break
        if empty_group:
            stages_stat.pop(group, None)
            ketamines_stat.pop(group, None)

    global COLORS
    COLORS = {stage:0 for stage in stages_stat[list(stages_stat.keys())[0]]}
    colors = ["#636568", "#d5deed", "#b8cdef", "#90b3ed", "#608edb",
              "#1d68e5", "#2f7bbf", "#872fbf", "#bf2fa9", "#bf2f6d"]
    c = 0
    for stage in COLORS:
        COLORS[stage] = colors[c]
        c+=1
    return stages_stat, ketamines_stat


def eerCounter(stages_stat, log_dict):
    group_errs={}
    for group in stages_stat:
        group_errs[group]=0
        if stages_stat[group] == {stage: 0 for stage in stages_stat[group]}:
            continue # pass the group if this is an empty group
        stage_sum = sum([stages_stat[group][stage] for stage in stages_stat[group]])
        max_stage = max(stages_stat[group], key=stages_stat[group].get)
        for stage in stages_stat[group]:
            # Error = the distance between stages * count of records in this stage / sum of all records in the group
            multiplier = abs(max_stage-int(stage))
            stage_value = stages_stat[group][stage]
            group_errs[group] += multiplier*stage_value/stage_sum
        group_errs[group]=round(group_errs[group],4)
        log_dict[group] = {stage:True if stage!=max_stage and stages_stat[group][stage]!=0
                           else False for stage in stages_stat[group]}
    return group_errs


# explode for all stages except the biggest
def explodeCalc(stages):
    if len(stages) == 0:
        return (0)
    index_of_max = stages.index(max(stages))
    explodes = []
    for i in range(len(stages)):
        explodes.append(0.1)
        if (i==index_of_max):
            explodes[i]=0
    return tuple(explodes)


def ketaminePlotter(fig, ketamine_stat):
    # Remove all empty groups
    for group in list(ketamine_stat):
        if ketamine_stat[group] == {stage: 0 for stage in ketamine_stat[group]}:
            ketamine_stat.pop(group, None)

    # sum of all used fragments
    all_fragments = sum([sum([ketamine_stat[group][stage] for stage in ketamine_stat[group]])
                         for group in ketamine_stat])

    # Calculate ratio of each stage for sum of all
    ketamine_percents = {}
    for group in ketamine_stat:
        ketamine_percents[group] = {stage: round(100 * (ketamine_stat[group][stage] / all_fragments), 2)
                                    for stage in ketamine_stat[group]}

    # Calculate errors
    log_dict = {}
    errors = eerCounter(ketamine_stat, log_dict)
    total_err = round(sum([errors[g] for g in errors]), 3)
    worst_group = max(errors, key=errors.get)
    if total_err == 0:
        worst_group = "None"

    # Plotting
    high, width = recSubPlotDet(len(ketamine_stat) + 1)
    i = 1
    for group in ketamine_stat:
        stage_positions = [stage for stage in ketamine_stat[group]]
        ketamine_percentage = [ketamine_percents[group][stage] for stage in stage_positions]

        plot = fig.add_subplot(high, width, i)
        plot.bar(stage_positions, ketamine_percentage, color=KETAMINE_COLOR)
        plot.set_xticks(stage_positions)

        # Title
        if group == worst_group:
            title_color = 'r'
        else:
            title_color = 'k'
        title = "{} ; error = {}".format(group, errors[group])
        plot.set_title(title, fontsize=10, color=title_color, position=(0.5, 0.9))

        # Axis
        if i==1:
            plot.set_ylabel("Percentage")
        plot.axis([stage_positions[0] - 0.5, stage_positions[-1] + 0.5, 0, 100])


        # Values on bars
        for k in range(len(stage_positions)):
            if ketamine_percentage[k] == 0:
                continue
            plot.text(stage_positions[k], ketamine_percentage[k] + 1, str(round(ketamine_percentage[k], 2)),# Full value
                      color=KETAMINE_COLOR, ha='center')
        i += 1

    # Pie plot of stage ratio
    plot = fig.add_subplot(high, width, high * width)

    all_stages_ratio = {}
    for group in ketamine_stat:
        for stage in ketamine_stat[group]:
            if stage not in all_stages_ratio:
                all_stages_ratio[stage] = 0
            all_stages_ratio[stage] += ketamine_stat[group][stage]
    values = [all_stages_ratio[stage] for stage in all_stages_ratio if all_stages_ratio[stage]!=0]
    all_names = [stage for stage in all_stages_ratio if all_stages_ratio[stage]!=0]
    colors = [COLORS[stage] for stage in COLORS if stage in all_names]

    plot.pie(values, labels=all_names, colors=colors)
    err_text = "Total error = {}\nThe worst group - {}".format(total_err, worst_group)
    plot.text(-1, -1.3, err_text, fontsize=10)
    title = "Distribution of all stages"
    plot.set_title(title, fontsize=10)
    plt.legend()
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, hspace=0.2, wspace=0.25)
    return log_dict


def histPlotter(fig, stages_stat_, ketamine_stat_, stage_show, ketamine_only = False):
    fig.clf()
    stages_stat = copy.deepcopy(stages_stat_)
    ketamine_stat = copy.deepcopy(ketamine_stat_)

    # Remove all invisible stages
    for stage in stage_show:
        if stage_show[stage] == False:
            for group in stages_stat:
                stages_stat[group].pop(stage, None)
                ketamine_stat[group].pop(stage, None)

    if ketamine_only: # plot with only ketamine
        return ketaminePlotter(fig, ketamine_stat)

    # Remove all empty groups
    for group in list(stages_stat):
        if stages_stat[group] == {stage: 0 for stage in stages_stat[group]}:
            stages_stat.pop(group, None)
            ketamine_stat.pop(group, None)


    # sum of all used fragments
    all_fragments = sum([sum([stages_stat[group][stage] for stage in stages_stat[group]]) for group in stages_stat])

    # Calculate ratio of each stage for sum of all
    stage_percents = {}
    ketamine_percents = {}
    for group in stages_stat:
        stage_percents[group] = {stage: round(100*(stages_stat[group][stage]/all_fragments), 2)
                              for stage in stages_stat[group]}
        ketamine_percents[group] = {stage: round(100*(ketamine_stat[group][stage]/all_fragments), 2)
                              for stage in ketamine_stat[group]}

    # Calculate errors
    log_dict = {}
    errors = eerCounter(stages_stat, log_dict)
    total_err = round(sum([errors[g] for g in errors]),3)
    worst_group = max(errors, key=errors.get)
    if total_err == 0:
        worst_group = "None"

    # Plotting
    high, width = recSubPlotDet(len(stages_stat)+1)
    i=1
    for group in stages_stat:
        stage_positions = [stage for stage in stages_stat[group]]
        ketamine_percentage = [ketamine_percents[group][stage] for stage in stage_positions]
        stage_percentage = [stage_percents[group][stage] for stage in stage_positions]

        plot = fig.add_subplot(high, width, i)
        plot.bar(stage_positions, stage_percentage, color=BAR_COLOR)
        plot.bar(stage_positions, ketamine_percentage, color=KETAMINE_COLOR)
        plot.set_xticks(stage_positions)

        # Title
        if group==worst_group:
            title_color='r'
        else:
            title_color='k'
        title = "{} ; error = {}".format(group, errors[group])
        plot.set_title(title, fontsize=10, color = title_color, position=(0.5, 0.88))

        # Axis
        if i==1:
            plot.set_ylabel("Percentage")
        plot.axis([stage_positions[0] - 0.5, stage_positions[-1] + 0.5, 0, 100])

        # Values on bars
        for k in range(len(stage_positions)):
            if stage_percentage[k] == 0:
                continue
            indentation = 1
            if ketamine_percentage[k]!=0:
                indentation = 5

            plot.text(stage_positions[k], stage_percentage[k] + indentation, str(round(stage_percentage[k], 2)), # Full value
                          color=BAR_COLOR, ha='center')
            if ketamine_percentage[k] == 0:
                continue
            plot.text(stage_positions[k], stage_percentage[k] + 1, str(round(ketamine_percentage[k], 2)),  # Value of ketamine fragments
                      color=KETAMINE_COLOR, ha='center')
        i+=1


    # Pie plot of stage ratio
    plot = fig.add_subplot(high, width, high*width)

    all_stages_ratio = {}
    for group in stages_stat:
        for stage in stages_stat[group]:
            if stage not in all_stages_ratio:
                all_stages_ratio[stage] = 0
            all_stages_ratio[stage] += stages_stat[group][stage]
    values = [all_stages_ratio[stage] for stage in all_stages_ratio if all_stages_ratio[stage]!=0]
    all_names = [stage for stage in all_stages_ratio if all_stages_ratio[stage]!=0]
    colors = [COLORS[stage] for stage in COLORS if stage in all_names]

    plot.pie(values, labels = all_names, colors = colors)
    err_text = "Total error = {}\nThe worst group - {}".format(total_err, worst_group)
    plot.text(-1,-1.3, err_text, fontsize=10)
    title = "Distribution of all stages"
    plot.set_title(title, fontsize=10, position=(0.5, 0.95))
    plt.legend()
    fig.subplots_adjust(left = 0.05, bottom = 0.05, right = 0.95, top = 0.95, hspace=0.2, wspace=0.25)
    return log_dict



