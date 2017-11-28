import os
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.widgets
from tkinter import Tk, Frame, LEFT, RIGHT, W, Checkbutton, Message, Button, BooleanVar, Canvas, PhotoImage, E
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showwarning


STAGES = [-1, 0, 1, 2, 3, 4, 5, 6, 7]
STAGE_NAMES = ["Artifacts", "Wakefulness", "First stage", "Second stage", "Third stage", "Fourth stage", "Fifth stage",
         "Sixth stage", "Seventh stage"]



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
    def __init__(self, matfile_name: str, report: str = None, stage: int = None, ketamine: bool = None):
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


class Checkbar(Frame):
    def __init__(self, parent, check_buttons, side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for button in check_buttons:
            chk = Checkbutton(self, text=str(button), variable=check_buttons[button])
            chk.pack(side=side, anchor=anchor)
            if (check_buttons[button].get()==True):
                chk.select()
            self.vars.append(check_buttons[button])

    def state(self):
        return list(map(lambda var: var.get(), self.vars))



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
    reports = [Report(report, readCSV(report)) for report in reports_list if report!=[]]
    correct_reports = [r for r in reports  if r.correct_report == True]
    incorrect_reports = [r for r in reports if r.correct_report == False]
    group_names = list(results.keys())
    for group in group_names:
        for matfile in range(len(results[group])):
            if results[group][matfile][:3]!="rec":
                results[group][matfile] = getStage("folder_" + results[group][matfile], correct_reports)
            else:
                results[group][matfile] = getStage(results[group][matfile], correct_reports)

    if incorrect_reports!=[]:
        err_msgs=["File: " + report.name + ", reason: " + report.reason for report in incorrect_reports ]
        warningMsg(err_msgs)
    return results


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
                write2csv(csv, group + ' stage ' + str(stage), save_path)
            except:
                write2csv(csv, group + ' stage ' + str(stage))


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
Window asking for ignored stages
'''
def askForStageIgnore():
    root = Tk()
    root.title("Stage ignore")
    ignore_list = {s:BooleanVar() for s in STAGES}

    def initiation():
        for s in ignore_list:
            ignore_list[s].set(stage_ignore[s])
    initiation()

    instructions = "Select the stages that should not be taken into account in statistics." \
                   " Stage -1 is an artefacts stage which means that an eeg record was corrupted by artifacts," \
                   " stage 0 is wakefulness."
    Message(root, text=instructions, width=300).pack(anchor=W, expand=True)
    Message(root, text="Stage: ").pack(anchor=W)

    ignored_stages=Checkbar(root, ignore_list)
    ignored_stages.pack()

    def cancelAndReset():
        initiation()
        root.destroy()

    def okClick():
        for s in stage_ignore:
            stage_ignore[s]=ignore_list[s].get()
        root.destroy()

    Button(root, text="Cancel", command=cancelAndReset).pack(side=RIGHT)
    Button(root, text="Ok", command=okClick).pack(side=LEFT)
    root.mainloop()




def getWorkingStages(eeg_fragments: dict, stage_ignore: dict):
    stages_stat = {}
    working_stages = [stage for stage in STAGES if stage not in stage_ignore]
    for group in eeg_fragments:
        stages_stat[group] = {stage:0 for stage in STAGES if stage not in stage_ignore}
        for eeg_fragment in eeg_fragments:
            if eeg_fragment.stage in working_stages:
                stages_stat[eeg_fragment.stage]+=1
        if stages_stat[group] == {stage:0 for stage in STAGES if stage not in stage_ignore}:
            stages_stat.pop(group, None)
    return stages_stat




'''
Plots histograms for each non empty group and save them to the result's folder
'''
def subPlotter(eeg: dict, stage_ignore: dict, save_path: str):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    local_stages = [stage for stage in STAGES if stage not in [int(stage) for stage in stage_ignore if
                                                               stage_ignore[stage]==True]]

    sum_of_fragments = sum([len([fragment for fragment in eeg[group] if (fragment.stage is not None) and
                                 (fragment.stage in local_stages)]) for group in eeg])

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


    group_errs={}
    for group in bar_values:
        group_errs[group]=0
        for stage in bar_values[group]:
            mult = abs(max(bar_values[group], key=bar_values[group].get)-int(stage))
            stage_val = bar_values[group][stage]
            stage_sum = sum([bar_values[group][v] for v in bar_values[group]])
            group_errs[group] += mult*stage_val/stage_sum
        group_errs[group]=round(group_errs[group],4)
    total_err = round(sum([group_errs[g] for g in group_errs]),3)
    worst_group = max(group_errs, key=group_errs.get)



    def checkBarWindow():
        root = Tk()
        root.title("Reports generating")

        instructions = "Select the elements in the groups for which you want to generate reports" \
                       " with the names of the files"
        Message(root, text=instructions, width=240).pack(anchor=W)

        groups = list(bar_values.keys())
        groups = {group: {str(stage): BooleanVar() for stage in local_stages} for group in groups}


        interested_stages = []
        for group in groups:
            Message(root, text=group, width=100).pack(anchor=W)
            interested_stages.append(Checkbar(root, groups[group]))
            interested_stages[-1].pack()

        def cancelAndReset():
            for g in groups:
                for s in groups[g]:
                    groups[g][s].set(False)
            root.destroy()

        Button(root, text="Cancel", command=cancelAndReset).pack(side=RIGHT)

        Button(root, text="Ok", command=root.destroy).pack(side=LEFT)

        root.mainloop()

        for g in groups:
            for s in groups[g]:
                groups[g][s] = groups[g][s].get()

        return {g: [int(stage) for stage in groups[g] if groups[g][stage]==True] for g in groups}


    '''
    Plotting
    '''
    high, width=recSubPlotDet(len(bar_values)+1)


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
    plt.show(block=False)
    interested_files = checkBarWindow()

    writeCSVforInterestedFiles(interested_files, eeg_fragments, save_path)

    matplotlib.rcParams.update({"font.size": 18})
    plt.savefig(save_path+"\\HIST.jpg", dpi=300)


'''
Start window frame
'''
def startWindow():
    def endProg():
        root.destroy()
        exit(0)

    root = Tk()
    root.title("EEG fragments analysis helper")

    introduction = "This script will build histograms of stage distribution for each column in a given csv or xlsx file."
    intr = Message(root, width=750, text=introduction)
    intr.config(font=(12))
    intr.grid(row=0, ipadx=15, ipady=15, sticky=W)

    instructions = "Please check that all eeg fragments are named like:\n" \
                   "folder name_YYYYMMDD_hh.mm.ss(start seconds from beginning-finish seconds from beginning)\n\n" \
                   "Example:"
    inst = Message(root, width=750, text=instructions)
    inst.config(font=("times", 14))
    inst.grid(row=1, ipadx=15, sticky=W)

    canvas_width = 770
    canvas_height = 142
    canvas = Canvas(root, width=canvas_width, height=canvas_height, borderwidth=4, relief="groove")
    canvas.grid(row=2, padx=10)
    img = PhotoImage(file="e:\\Users\\sevamunger\\Desktop\\example.png")
    canvas.create_image(5, 75, anchor=W, image=img)

    continue_button = Button(root, text="Exit", width=10, command=endProg, borderwidth=3)
    continue_button.grid(row=3, column=0, sticky=E, padx=20, pady=10)
    exit_button = Button(root, text="Continue", width=16, command=root.destroy, borderwidth=3)
    exit_button.grid(row=3, column=0, sticky=W, padx=40, pady=10)
    root.mainloop()



if __name__ == "__main__":
    '''''''''''''''''
    # Preparing files
    '''''''''''''''''

    startWindow()

    path_to_results = "Z:\\Tetervak\\21_data16_2_5min_20171116_143200.csv"
    path_to_reports = "Z:\\Tetervak\\Reports\\complete"
    results, save_path = resultReader(path_to_results)
    reports_list = reportReader(path_to_reports)


    eeg_fragments = matfiles2eegFragments(results, reports_list)  # returns the dictionary of eeg objects

    # percentage of processed records for the each group
    processed_records = [(len(eeg_fragments[g]) - len([eeg for eeg in eeg_fragments[g] if eeg.stage == None])) /
                         len(eeg_fragments[g]) if len(eeg_fragments[g]) != 0 else -1 for g in eeg_fragments]

    stage_ignore = {-1:True, 0:False, 1:False, 2:False, 3:False, 4:True, 5:True, 6:True, 7:True}
    exit(12)
    askForStageIgnore()


    subPlotter(eeg_fragments, stage_ignore,save_path)



