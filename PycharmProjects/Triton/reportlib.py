#!/usr/bin/env python3


import os
import pandas
import datetime
import pickle
import numpy as np
import pandas as pd


STAGES = [-1, 0, 1, 2, 3, 4, 5, 6, 7]  # -1 is a state with artefacts, 0 - wakefulness and so on
STAGE_AI = {-1: -1, 0: 95, 1: 85, 2: 70, 3: 50, 4: 30, 5: 20, 6: 10, 7: 0}  # corresponding AI for the middle of a stage


def countMedicine(med_column):
    """
    Counts all medicine used in an operation
    :param med_column: Column in which all used medicine presents
    :return: String of medicine by comma
    """
    med_cells = [cell for cell in med_column if not pandas.isnull(cell)]
    medicine = []
    for cell in med_cells:
        for med in cell.split(','):
            if med not in medicine:
                medicine.append(med.replace(' ', ''))
    return ', '.join(medicine)


def timeFormat(time_stamps, file_name):
    """

    :param time_stamps: report table with values of time and stage
    :param file_name:  A file name or path to a file
    :return:
    """
    date = file_name.split('_')[-1]  # something like rec002_300409.csv
    second_stamps = []
    for t in time_stamps["Time"]:
        time = t.split(':')
        second_stamps.append(
            int(datetime.datetime(int("20" + date[4:6]), int(date[2:4]), int(date[0:2]),  # YYYY, MM, DD
                                  int(time[0]), int(time[1]), int(time[2])).timestamp()))  # HH, MM, SS

    if second_stamps != sorted(second_stamps):
        print("Wrong time order")
        exit(33)

    ai = []
    for stage in time_stamps["Stage"]:
        ai.append(stage)

    sec_stage = [second_stamps[0]]  # the first element is a start second
    for i in range(len(second_stamps) - 1):
        step = int(second_stamps[i + 1] - second_stamps[i])
        for k in range(step):
            sec_stage.append(STAGE_AI[ai[i]])  # append stage value for each second
    return np.array(sec_stage)


class Fragment(object):
    def __init__(self, fragment_name, ai=None):
        rec, ymd, hms = fragment_name.split('_')
        year = ymd[:4]
        month = ymd[4:6]
        day = ymd[6:]
        hms = hms.split('(')[0]
        hour, minute, second = hms.split('.')
        start_second = int(datetime.datetime(int(year), int(month), int(day),
                                             int(hour), int(minute), int(second)).timestamp())
        time_delta = fragment_name.split('(')[-1].split(')')[0]
        self.name = fragment_name
        self.record = rec
        self.start, self.end = time_delta.split('-')
        self.start = start_second + int(self.start)
        self.end = start_second + int(self.end)
        self.ai = ai


class ReportAI(object):
    def __init__(self, path_to_report):
        wb = pandas.read_csv(path_to_report, delimiter=';').dropna(axis=0, how='all')
        self.doctor = wb["Doctor"][0] if not pandas.isnull(wb["Doctor"][0]) else "Unknown"
        self.diagnosis = wb["Diagnosis"][0] if not pandas.isnull(wb["Diagnosis"][0]) else "Unknown"
        self.electrodes_position = wb["Position"][0] if not pandas.isnull(wb["Position"][0]) else "Unknown"
        self.medicines = countMedicine(wb["Medicine"])
        self.comment = wb["Overall comment"][0] if not pandas.isnull(wb["Overall comment"][0]) else "No comments"
        time_stage = timeFormat(wb[["Time", "Stage"]], os.path.basename(path_to_report))
        self.date = time_stage[0]  # The first element in time_stage is the first second of a record
        self.time = time_stage[0] + np.arange(len(time_stage) - 1)
        self.ai = time_stage[1:]  # The first element in time_stage is the first second of a record
        self.record_number = os.path.basename(path_to_report).split('_')
        self.record = [i for i in self.record_number if i[0:3] == "rec"][0]

    def getAi(self, start_second, end_second):
        if self.time[0] > start_second or end_second > self.time[-1]:
            return None
        start = start_second - self.time[0]
        time_delta = end_second - start_second
        average_ai = 0
        for i in range(time_delta):
            if self.ai[start + i] == -1:  # if found at artifact - this fragment is artifacted
                return -1  # return artifacted ai
            average_ai += self.ai[start + i]
        average_ai /= time_delta
        return round(average_ai, 1)

    def setAi(self, start_second, end_second, ai):
        if self.time[0] > start_second:
            if self.time[0] < end_second:
                for i in range(end_second - self.time[0]):
                    self.ai[i] = ai
                return True
            else:
                return False  # if an entire fragment is out of report

        if self.time[-1] < end_second:
            if self.time[-1] > start_second:
                for i in range(self.time[-1] - start_second):
                    self.ai[-i - 1] = ai
                return True
            else:
                return False  # if an entire fragment is out of report

        start_index = start_second - self.date
        for i in range(end_second - start_second):
            self.ai[start_index + i] = ai
        return True

    def saveToPickle(self, path_to_save="Z:\\Tetervak\\Reports\\reports 2.0\\reports_pickle"):
        pickle_output = open(os.path.join(path_to_save, "{}.{}".format(self.record, 'pickle')), 'wb')
        pickle.dump(self, pickle_output)
        pickle_output.close()


if __name__ == "__main__":
    print("Reportlib is a definition of ReportAI and Fragment classes.")