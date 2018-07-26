import matplotlib.pyplot as plt
import os
import pickle
import datetime
import pandas


STAGE_AI = {-1: -1, 0: 97, 1: 85, 2: 70, 3: 50, 4: 30, 5: 20, 6: 10, 7: 0}


class ReportAI(object):
    def __init__(self, path_to_report):
        wb = pandas.read_csv(path_to_report, delimiter=';').dropna(axis=0, how='all')

        self.doctor = wb["Doctor"][0] if not pandas.isnull(wb["Doctor"][0]) else "Unknown"
        self.diagnosis = wb["Diagnosis"][0] if not pandas.isnull(wb["Diagnosis"][0]) else "Unknown"
        self.electrodes_position = wb["Position"][0] if not pandas.isnull(wb["Position"][0]) else "Unknown"
        self.medicines = medicineCounter(wb["Medicine"])
        self.comment = wb["Overall comment"][0] if not pandas.isnull(wb["Overall comment"][0]) else "No comments"

        time_stage = timeFormat(wb[["Time", "Stage"]], os.path.basename(path_to_report))
        self.time = [second + time_stage[0] for second in range(len(time_stage) - 1)]
        self.stages = time_stage[1:]  # The first element in time_stage is the first second of a record
        self.date = time_stage[0]  # The first element in time_stage is the first second of a record

        record_number = os.path.basename(path_to_report).split('_')
        record_number = [i for i in record_number if i[0:3] == "rec"][0]
        self.record_name = record_number

    def saveToPickle(self, path_to_save="Z:\\Tetervak\\Reports\\reports 2.0\\reports_pickle"):
        pickle_output = open(os.path.join(path_to_save, "{}.{}".format(self.record_name, '.pickle')), 'wb')
        pickle.dump(self, pickle_output)
        pickle_output.close()


class FragmentList(object):
    def __init__(self, path_to_fragments):
        self.fragments = []
        with open(path_to_fragments, 'r') as file:
            for line in file:
                self.fragments.append(line.replace('\n', '').replace(';', ''))

        self.time_step = 300
        if '(' in self.fragments[0]:
            self.time_step = self.fragments[0].split('(')[-1].split(')')[0].split('-')  # xxx(90-120)xxx
            self.time_step = int(self.time_step[-1]) - int(self.time_step[0])  # 120 - 90 = 30

    def fragments2pickle(self, path_to_save="Z:\\Tetervak\\Reports\\reports 2.0\\fragments_pickle"):
        pickle_output = open("{}\\{}_second_fragments.pickle".format(path_to_save, self.time_step), 'wb')
        pickle.dump(self, pickle_output)
        pickle_output.close()

    def rec_list(self, record_name):  # Returns start seconds of all fragments for the record
        return sorted([matName2Time(f) for f in self.fragments if f[:6] == record_name and
                       len(f.split('_')) == 3])  # return list for the record without records 000_1, 000_2


class BaredReport(object):
    def __init__(self, report, fragment_list):
        # Report information
        self.record_name = report.record_name
        self.fragment_times = fragment_list.rec_list(self.record_name)  # list of fragments start seconds
        self.time_step = fragment_list.time_step
        self.wakefulness_level = 100

        # Calculating bar values
        self.ai_values = []
        self.time_values = []
        for i in range(len(self.fragment_times)):
            if self.fragment_times[i] < report.time[0]:
                continue
            elif self.fragment_times[i] > report.time[-1]:
                break
            else:
                start_index = report.time.index(self.fragment_times[i])
                ai = 0
                step = fragment_list.time_step
                if self.fragment_times[i] + step > report.time[-1]:
                    step = report.time[-1] - self.fragment_times[i]
                for k in range(step):
                    ai += report.stages[start_index + k]
                self.ai_values.append(ai / step)
                self.time_values.append(self.fragment_times[i] + int(step/2))

        """
        TESTING VALUES
        """
        self.time_values = [self.time_values[0] + i * 30 for i in range(50)]
        self.ai_values = 5*[i + 1 for i in range(10)]
        """"""

        """
        Figure parameters
        """
        # Axis values
        self.bars_on_plot = 15
        self.ticks_on_plot = 8
        self.x_min = self.time_values[0] - self.time_step/2
        self.x_max = self.time_values[-1] + self.time_step/2
        if len(self.time_values) > self.bars_on_plot:
            self.x_max = self.time_values[self.bars_on_plot - 1] + self.time_step/2
        self.y_min = -5
        self.y_max = 110
        self.pan_x = None

    def updateTicks(self):
        self.x_ticks_names = []
        self.x_ticks = []
        tick_per_value = int(round(self.bars_on_plot / self.ticks_on_plot))
        for i in range(len(self.time_values)):
            if i % tick_per_value == 0:
                self.x_ticks.append(self.time_values[i])
                self.x_ticks_names.append(str(datetime.datetime.fromtimestamp(self.time_values[i]).time()))


def reportTime(string_time: str, report_path: str):  # convert string to time in the given report
    year = int("20" + report_path[-6:-4])
    month = int(report_path[-8:-6])
    day = int(report_path[-10:-8])
    point = ':'  # default delimiter
    for char in string_time:
        if char == '.':
            point = '.'
            break
        elif char == '-':
            point = '-'
            break
        elif char == '\\':
            point = '\\'
            break
        elif char == '/':
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
    elif (len(t) == 2):  # if there is one delimiter in the time
        if (len(t[0]) == 2 or len(t[0]) == 1) and len(t[1]) == 2:
            return datetime.datetime(year, month, day, int(t[0]), int(t[1]), 00)
        return ' '.join(["Wrong time format", ''.join(t)])
    elif (len(t) == 3):  # if there are two delimiters in the time
        if (len(t[0]) == 2 or len(t[0]) == 1) and len(t[1]) == 2 and len(t[2]) == 2:
            return datetime.datetime(year, month, day, int(t[0]), int(t[1]), int(t[2]))
        return ' '.join(["Wrong time format", ''.join(t)])
    return ' '.join(["Wrong time format", ''.join(t)])

def matName2Time(matfile_name: str) -> [datetime.datetime, int]:  # convert Mat file's name to date and time
    start_second = 0
    if '(' in matfile_name:
        time_delta = matfile_name.split('(')[1].split(')')[
            0]  # this will be the number of seconds since the fragment beginning
        start_second = int(time_delta.split('-')[0])  # if time delta looks like 100-120

    name = matfile_name.split('_')
    if '(' in name[-1]:
        name[-1] = name[-1].split('(')[0]

    dt = int((datetime.datetime(int(name[-2][0:4]), int(name[-2][4:6]), int(name[-2][6:8]),  # YYYY, MM, DD
               int(name[-1][:2]), int(name[-1][3:5]),  # HH, MM, SS
               int(name[-1][6:8])) + datetime.timedelta(seconds = start_second)).timestamp())
    return dt

def medicineCounter(med_table):
    med_cells = [cell for cell in med_table if not pandas.isnull(cell)]
    medicines = []
    for cell in med_cells:
        for med in cell.split(','):
            if med not in medicines:
                medicines.append(med.replace(' ', ''))
    return ', '.join(medicines)

def timeFormat(time_stamps, file_name):
    date = file_name.split('_')[-1]
    second_stamps = []
    for t in time_stamps["Time"]:
        time = t.split(':')
        second_stamps.append(
            int(datetime.datetime(int("20" + date[4:6]), int(date[2:4]), int(date[0:2]),  # YYYY, MM, DD
                                  int(time[0]), int(time[1]), int(time[2])).timestamp()))  # HH, MM, SS

    if second_stamps != sorted(second_stamps):
        print("Wrong time order")
        exit(33)

    stages = []
    for stage in time_stamps["Stage"]:
        stages.append(stage)

    sec_stage = [second_stamps[0]]  # the first element is a start second
    for i in range(len(second_stamps) - 1):
        step = int(second_stamps[i + 1] - second_stamps[i])
        for k in range(step):
            sec_stage.append(STAGE_AI[stages[i]])  # append stage for each second
    return sec_stage

def fragmentUpdating(path_to_txts = "Z:\\Tetervak\\Reports\\reports 2.0\\fragments_txt",
                   path_to_pickles = "Z:\\Tetervak\\Reports\\reports 2.0\\fragments_pickle"):
    # Find all pickle fragments
    pickle_fragments = [f.split('_')[0] for f in os.listdir(path_to_pickles)
                   if os.path.isfile(os.path.join(path_to_pickles, f))]
    txt_fragments = [f for f in os.listdir(path_to_txts)
                   if os.path.isfile(os.path.join(path_to_txts, f))]
    # Find all fragments lists which don't have a pickle version
    for f in txt_fragments:
        if f.split('_')[0] not in pickle_fragments:
            FragmentList(os.path.join(path_to_txts, f)).fragments2pickle()

def reportUpdating(path_to_csvs = "Z:\\Tetervak\\Reports\\reports 2.0\\reports_csv",
                   path_to_pickles = "Z:\\Tetervak\\Reports\\reports 2.0\\reports_pickle"):
    # Find all pickle reports
    pickle_reports = [f.split('.')[0] for f in os.listdir(path_to_pickles)
                   if os.path.isfile(os.path.join(path_to_pickles, f))]
    csv_reports = [f for f in os.listdir(path_to_csvs)
                   if os.path.isfile(os.path.join(path_to_csvs, f))]

    # Find all completed reports which don't have an txt version
    for f in csv_reports:
        if f.split('_')[0] not in pickle_reports:
            ReportAI(os.path.join(path_to_csvs, f)).saveToPickle()

def onClick(event, axis, report):
    if event.xdata is not None and event.ydata is not None and event.button == 1:
        for i in range(len(report.time_values)):
            if abs(event.xdata - report.time_values[i]) <= report.time_step/2:
                report.ai_values[i] = int(event.ydata)
        axis.clear()
        drawBars(axis, report)
        axis.figure.canvas.draw()
    if event.xdata is not None and event.ydata is not None and event.button == 3:
        if True:
            report.pan_x = event.xdata

def onScroll(event, axis, report):
    if event.button == "up":
        report.bars_on_plot += 1
        report.x_max += report.time_step
        axis.clear()
        drawBars(axis, report)
        axis.figure.canvas.draw()
    if event.button == "down":
        report.bars_on_plot -= 1
        report.x_max -= report.time_step
        axis.clear()
        drawBars(axis, report)
        axis.figure.canvas.draw()

def onMovement(event, axis, report):
    if event.xdata is not None and event.ydata is not None and event.button == 1:
        for i in range(len(report.time_values)):
            if abs(event.xdata - report.time_values[i]) <= report.time_step/2:
                report.ai_values[i] = int(event.ydata)
        axis.clear()
        drawBars(axis, report)
        axis.figure.canvas.draw()
    elif event.xdata is not None and event.ydata is not None and event.button == 3 and report.pan_x is not None:
        report.x_max -= event.xdata - report.pan_x
        report.x_min -= event.xdata - report.pan_x
        if report.x_min < report.time_values[0]  - report.time_step/2:
            report.x_min = report.time_values[0]  - report.time_step/2
            report.x_max = report.time_values[0] + report.time_step / 2 + report.time_step * report.bars_on_plot
        if report.x_max > report.time_values[-1]  + report.time_step/2:
            report.x_max = report.time_values[-1] + report.time_step / 2
            report.x_min = report.time_values[-1] - report.time_step / 2 - report.time_step * report.bars_on_plot

        axis.clear()
        drawBars(axis, report)
        axis.figure.canvas.draw()

def drawBars(axis, report):
    report.updateTicks()
    start_bar = 0 # Find the first visible bar
    while(report.time_values[start_bar] < report.x_min):
        start_bar += 1
    last_bar = start_bar + report.bars_on_plot if len(report.time_values) > start_bar + report.bars_on_plot \
        else len(report.time_values) - 1 # Find the last visible bar

    for i in range(start_bar, last_bar): # Add value for the each visible bar
        axis.text(report.time_values[i], report.ai_values[i] + 2, "{}".format(report.ai_values[i]), ha='center')

    axis.plot([report.time_values[start_bar] - report.time_step, report.time_values[last_bar] + report.time_step],
              [report.wakefulness_level, report.wakefulness_level], color = 'red', linestyle='--', dashes=(5, 10))

    bar_list = axis.bar(report.time_values[start_bar: last_bar],
             report.ai_values[start_bar: last_bar],
             width = report.time_step - 1)

    for bar in bar_list:
        if bar._height < 0:
            bar.set_color('r')
        elif bar._height > 100:
            bar.set_color('y')


    axis.set_xticks(report.x_ticks)
    axis.set_xticklabels(report.x_ticks_names)
    axis.axis([report.x_min, report.x_max,
               report.y_min, report.y_max])
    axis.set_title(report.record_name)

if __name__ == "__main__":
    fragmentUpdating()
    reportUpdating()

    path_to_reports = "Z:\\Tetervak\\Reports\\reports 2.0\\reports_pickle"
    path_to_fragments = "Z:\\Tetervak\\Reports\\reports 2.0\\fragments_pickle"

    reports = [pickle.load(open(os.path.join(path_to_reports, pck), 'rb')) for pck in os.listdir(path_to_reports)
               if os.path.isfile(os.path.join(path_to_reports, pck))]
    fragments = [pickle.load(open(os.path.join(path_to_fragments, pck), 'rb')) for pck in os.listdir(path_to_fragments)
               if os.path.isfile(os.path.join(path_to_fragments, pck))]

    test_report = reports[0]
    test_fragment = fragments[0]

    test_bar_report = BaredReport(test_report, test_fragment)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fig.canvas.mpl_connect('button_press_event', lambda event: onClick(event, axis=ax, report=test_bar_report))
    fig.canvas.mpl_connect('scroll_event', lambda event: onScroll(event, axis=ax, report=test_bar_report))
    fig.canvas.mpl_connect('motion_notify_event', lambda event: onMovement(event, axis=ax, report=test_bar_report))
    drawBars(ax, test_bar_report)
    plt.show()






















