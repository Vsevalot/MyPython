import datetime
import pandas
import os
import pickle

STAGE_AI = {-1:-1, 0: 97, 1:85, 2:70, 3:50, 4:30, 5:20, 6:10, 7:0}

class ReportAI(object):
    def __init__(self, record, diagnosis, doctor, position, medicines, comment, time_stage):
        self.record_number = record
        self.diagnosis = diagnosis
        self.doctor = doctor
        self.electrodes_position = position
        self.medicines = medicines
        self.comment = comment
        self.time = [second + time_stage[0] for second in range(len(time_stage) - 1)]
        self.stages = time_stage[1:]

    def saveToPickle(self, path_to_save):
        pickle_output = open("{}\\{}.pickle".format(path_to_save, self.record_number), 'wb')
        pickle.dump(self, pickle_output)
        pickle_output.close()


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
    if (len(t) == 2):  # if there is one delimiter in the time
        if (len(t[0]) == 2 or len(t[0]) == 1) and len(t[1]) == 2:
            return datetime.datetime(year, month, day, int(t[0]), int(t[1]), 00)
        return ' '.join(["Wrong time format", ''.join(t)])
    if (len(t) == 3):  # if there are two delimiters in the time
        if (len(t[0]) == 2 or len(t[0]) == 1) and len(t[1]) == 2 and len(t[2]) == 2:
            return datetime.datetime(year, month, day, int(t[0]), int(t[1]), int(t[2]))
        return ' '.join(["Wrong time format", ''.join(t)])
    return ' '.join(["Wrong time format", ''.join(t)])

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
        second_stamps.append(int(datetime.datetime(int("20" + date[4:6]), int(date[2:4]), int(date[0:2]), # YYYY, MM, DD
                           int(time[0]), int(time[1]), int(time[2])).timestamp())) # HH, MM, SS

    if second_stamps != sorted(second_stamps):
        print("Wrong time order")
        exit(33)

    stages = []
    for stage in time_stamps["Stage"]:
        stages.append(stage)

    sec_stage = [second_stamps[0]] # the first element is a start second
    for i in range(len(second_stamps) - 1):
        step = int(second_stamps[i+1] - second_stamps[i])
        for k in range(step):
            sec_stage.append(stages[i]) # append stage for each second
    return sec_stage

def report2pickle(report, path_to_save = "Z:\\Tetervak\\Reports\\reports 2.0\\pickle_reports"):
    wb = pandas.read_csv(report, delimiter=';').dropna(axis=0, how='all')
    doctor = wb["Doctor"][0] if not pandas.isnull(wb["Doctor"][0]) else "Unknown"
    diagnosis = wb["Diagnosis"][0] if not pandas.isnull(wb["Diagnosis"][0]) else "Unknown"
    position = wb["Position"][0] if not pandas.isnull(wb["Position"][0]) else "Unknown"
    medicines = medicineCounter(wb["Medicine"])
    comment = wb["Overall comment"][0] if not pandas.isnull(wb["Overall comment"][0]) else "No comments"

    time_stage = timeFormat(wb[["Time", "Stage"]], os.path.basename(report))

    record_number = os.path.basename(report).split('_')
    record_number = [i for i in record_number if i[0:3] == "rec"][0]

    report = ReportAI(record = record_number,
                      diagnosis = diagnosis,
                      position = position,
                      medicines = medicines,
                      doctor = doctor,
                      comment = comment,
                      time_stage = time_stage)

    report.saveToPickle(path_to_save)

if __name__ == "__main__":
    path_to_reports = "Z:\\Tetervak\\Reports\\reports 2.0\\complete"
    report_list = [os.path.join(path_to_reports, f) for f in os.listdir(path_to_reports)
                   if os.path.isfile(os.path.join(path_to_reports, f))]

    for r in report_list:
        report2pickle(r)

    pickle_input = open("Z:\\Tetervak\\Reports\\reports 2.0\\pickle_reports\\rec002.pickle", 'rb')
    test = pickle.load(pickle_input)
    print(test.record_number)








