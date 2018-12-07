#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import numpy as np
import sys
import os
import pickle
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFileDialog
from reportlib import Fragment, ReportAI


def intersperse(array, item):  # inserts an item between all elements of a list
    result = [item] * (len(array) * 2 - 1)
    result[::2] = array
    return result


def removeRepeating(name_arr): # remove repeating from the "name" column
    x = name_arr
    i = 1
    while i < len(x):
        if x[i] is None:
            i += 2
            if i >= len(x):
                break
        x[i] = None
        i += 1
    return x


def justName(matfile_name: str) -> str:
    return matfile_name.split('_')[0][1:]


def matName2Time(matfile_name: str) -> [datetime.datetime, int]:  # convert Mat file's name to date and time
    if type(matfile_name) == float:
        return np.nan
    start_second = 0
    if '(' in matfile_name:
        time_delta = matfile_name.split('(')[1].split(')')[0]  # the number of seconds since the fragment beginning
        start_second = int(time_delta.split('-')[0])  # if time delta looks like 100-120

    name = matfile_name.split('_')
    if '(' in name[-1]:
        name[-1] = name[-1].split('(')[0]

    dt = int((datetime.datetime(int(name[-2][0:4]), int(name[-2][4:6]), int(name[-2][6:8]),  # YYYY, MM, DD
                                int(name[-1][:2]), int(name[-1][3:5]), int(name[-1][6:8]))  # HH, MM, SS
              + datetime.timedelta(seconds=start_second)).timestamp())
    return dt


def findInStreak(err_df, streak=3):  # in_row parameter - the number of fragments in row which must be noted as anomaly
    records = list(err_df["fragment"])
    seconds = list(err_df["start_second"])
    time_stamp = records[0].split('(')[-1].split(')')[0].split('-')
    time_stamp = int(time_stamp[1]) - int(time_stamp[0])
    diff = streak - 1
    closest = [False] * len(records)
    fragments = []
    i = 0
    while i < len(records) - diff:
        if records[i].split('_')[0][1:] == records[i+diff].split('_')[0][1:]:  # If there are diff exemplars of a record
            if seconds[i] >= seconds[i + diff] - diff*time_stamp:  # If these exemplars stay close to each other in time
                closest[i] = True
                i += 1
                fragments.append([records[i].split('_')[0], datetime.datetime.fromtimestamp(seconds[i]).time()])
                while seconds[i] - seconds[i-1] <= time_stamp:
                    closest[i] = True
                    i += 1
                fragments[-1].append(datetime.datetime.fromtimestamp(seconds[i]).time())
                continue
        i += 1

    streaks = [None] * len(records)
    for i in range(len(closest) - 1):
        if closest[i]:
            if not closest[i + 1]:
                streaks[i] = "last"
                continue
            streaks[i] = "streak"
    if closest[-1]:  # if last element is a part of a streak -> it's the last element of the streak
        streaks[-1] = "last"

    return streaks


def addStatisctic(data_frame):
    records = data_frame["rec"].values
    records = [records[0]] + [None] * (len(records) - 1)
    statistic_dict = {column: [None] * 3 for column in data_frame.columns}
    statistic_dict["rec"][0] = "Mean"
    statistic_dict["rec"][1] = "STD"
    mean_exp = round(np.mean(data_frame["expected_AI"]), 1)
    mean_calc = round(np.mean(data_frame["calculated_AI"]), 1)
    statistic_dict["expected_AI"][0] = mean_exp
    statistic_dict["calculated_AI"][0] = mean_calc
    statistic_dict["expected_AI"][1] = round(np.std(data_frame["expected_AI"]), 1)
    statistic_dict["calculated_AI"][1] = round(np.std(data_frame["calculated_AI"]), 1)
    statistic_dict["time"][0] = round(mean_exp - mean_calc, 1)
    final = data_frame
    final.is_copy = False
    final["rec"] = records
    final = final.append(pd.DataFrame.from_dict(statistic_dict), ignore_index=True)
    final["fixed_ai"] = final["expected_AI"] - round(mean_exp - mean_calc, 1)
    return final


class CorrectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.loadData()
        self.initUI()


    def initUI(self):
        self.setGeometry(500, 500, 280, 270)
        self.setWindowTitle("File picker")
        self.correct_btn = QPushButton("Choose a folder with skipped.mat", self)
        self.correct_btn.clicked.connect(self.correction)
        self.correct_btn.setGeometry(100, 50, 150, 50)

        self.file_stage_btn = QPushButton("Generate file - stage", self)
        self.file_stage_btn.clicked.connect(self.generateFileStage)
        self.file_stage_btn.setGeometry(100, 150, 150, 50)
        self.show()


    def loadData(self):
        path_to_reports = "Z:/Tetervak/Reports/reports 2.0/reports_pickle"
        self.report_list = [r[:-7] for r in os.listdir(path_to_reports)]


    def correction(self):
        path_to_folder = QFileDialog.getExistingDirectory(self, "Choose a folder with skipped.mat to correct",
                                                          "Z:/Tetervak/skipped")
        if path_to_folder == '':  # if no file selected
            return

        if os.path.exists(os.path.join(path_to_folder, "more_15_errors.csv")):
            self.correctAI(path_to_folder)

        if os.path.exists(os.path.join(path_to_folder, "sigma6.csv")):
            self.sigmaIgnore(path_to_folder)

        if os.path.exists(os.path.join(path_to_folder, "broken_fragments.csv")):
            self.brokenIgnore(path_to_folder)

        print("Correction complete")


    def correctReports(self, fixed_df):
        fragments = list(fixed_df["fragment"].values)
        ai = list(fixed_df["fixed_ai"].values)
        fixed_fragments = [Fragment(fragments[i], ai[i]) for i in range(len(fragments))]

        report = None
        for fragment in fixed_fragments:
            if fragment.record in self.report_list:
                if report is None:
                    report = pickle.load(open("Z:/Tetervak/Reports/reports 2.0/reports_pickle/" \
                                              "{}.pickle".format(fragment.record), 'rb'))
                if fragment.record != report.record:
                    report.saveToPickle()
                    report = pickle.load(open("Z:/Tetervak/Reports/reports 2.0/reports_pickle/" \
                                              "{}.pickle".format(fragment.record), 'rb'))
                report.setAi(fragment.start, fragment.end, fragment.ai)

        if report is not None:  # if at least one report was opened
            report.saveToPickle()


    def correctAI(self, path_to_folder):
        column_names = ["fragment", "expected_stage", "expected_AI", "calculated_AI", "error"]
        df = pd.read_csv(os.path.join(path_to_folder, "more_15_errors.csv"), delimiter=';', names=column_names)
        df["name_len"] = df["fragment"].apply(lambda name: len(name.split('_')))  # remove rec020_1_... fragments
        df = df[df["name_len"] == 3]
        df = df.drop(["name_len"], axis=1)

        timestamp = df["fragment"][0].split('(')[1].split(')')[0].split('-')  # time stamp like str '90-120'
        timestamp = int(timestamp[-1]) - int(timestamp[0])  # time stamp like int 30
        df["start_second"] = df["fragment"].apply(matName2Time)  # form a column of fragment's start second
        df["end_second"] = df["start_second"] + timestamp
        df["rec"] = df["fragment"].apply(lambda x: x.split('_')[0])  # form a column of fragment's record
        df = df.sort_values(["rec", "start_second"])  # sort fragments by record and these fragments by time
        df.index = [i for i in range(len(df))]

        #  Searching for streaks
        df["streak"] = findInStreak(df)
        not_streak_df = df[df["streak"].isnull()]
        streak_df = df[df["streak"].notnull()]

        #  Working with not streaks, less than 30 error
        quick_fix_df = not_streak_df[not_streak_df["error"] <= 30]
        quick_fix_df.is_copy = False
        quick_fix_df["fixed_ai"] = (quick_fix_df["expected_AI"] + quick_fix_df["calculated_AI"]) / 2
        quick_fix_df["fixed_ai"] = quick_fix_df["fixed_ai"].apply(int)  # to avoid conflicts with excel float
        quick_fix_df.to_csv(os.path.join(path_to_folder, "single_fixed.csv"), sep=';',
                            encoding='utf-8', columns=["fragment", "fixed_ai"], index=False)
        self.correctReports(quick_fix_df)

        #  Working with not streaks, more than 30 error - artifacts
        big_error_df = not_streak_df[not_streak_df["error"] > 30]
        big_error_df.is_copy = False
        big_error_df["fixed_ai"] = [-1 for i in range(len(big_error_df["fragment"].values))]  # set ai to art. value
        big_error_df.to_csv(os.path.join(path_to_folder, "artifacts.csv"), sep=';', encoding='utf-8', index=False,
                            columns=["fragment"])
        self.correctReports(big_error_df)

        #  Working with not streaks, more than 30 error - artifacts
        streak_df.index = [i for i in range(len(streak_df))]
        streak_df.is_copy = False  # remove a SettingWithCopyWarning
        streak_df["time"] = streak_df["start_second"].apply(lambda x: datetime.datetime.fromtimestamp(x).time())
        streak_df["calculated_AI"] = streak_df["calculated_AI"].apply(int)
        split_indexes = [-1] + streak_df[streak_df["streak"] == "last"].index.tolist()  # needn't after the last streak
        split_df = [streak_df.iloc[split_indexes[i] + 1: split_indexes[i + 1] + 1] for i in
                    range(len(split_indexes) - 1)]
        for i in range(len(split_df)):
            split_df[i] = addStatisctic(split_df[i])
        csv_df = pd.concat(split_df, ignore_index=True)
        csv_df.to_csv(os.path.join(path_to_folder, "streaks_info.csv"), sep=';', encoding='utf-8', index=False,
                      columns=["rec", "expected_AI", "calculated_AI", "time"])  # visualisation of streaks
        fixed_streak = csv_df[csv_df["fragment"].notnull()]
        fixed_streak.is_copy = False
        fixed_streak["fixed_ai"] = fixed_streak["fixed_ai"].apply(int)  # to avoid conflicts with excel float
        fixed_streak.to_csv(os.path.join(path_to_folder, "streaks_fixed.csv"), sep=';', encoding='utf-8', index=False,
                            columns=["fragment", "fixed_ai"])
        self.correctReports(fixed_streak)


    def brokenIgnore(self, path_to_folder):
        broken_fragments = pd.read_csv(os.path.join(path_to_folder, "broken_fragments.csv"), delimiter=';', names=["fragment"])
        broken_fragments = list(broken_fragments["fragment"].values)
        if len(broken_fragments) == 0:
            return

        timestamp = broken_fragments[0].split('(')[1].split(')')[0].split('-')  # time stamp like str '90-120'
        timestamp = int(timestamp[-1]) - int(timestamp[0])  # time stamp like int 30

        ignore = []
        if os.path.exists(os.path.join("Z:/Tetervak/fragments", "broken_fragments_%d_sec.csv" % timestamp)):
            ignore = pd.read_csv(os.path.join("Z:/Tetervak/fragments", "broken_fragments_%d_sec.csv" % timestamp))
            ignore = list(ignore["fragment"].values)

        for fragment in broken_fragments:
            if fragment not in ignore:
                ignore.append(fragment)

        ignore = pd.DataFrame({"fragment": ignore})
        ignore.to_csv(os.path.join("Z:/Tetervak/fragments", "broken_fragments_{}_sec.csv".format(timestamp)),
                      index=False)


    def sigmaIgnore(self, path_to_folder):
        sigma = pd.read_csv(os.path.join(path_to_folder, "sigma6.csv"),delimiter=';', names=["fragment"])
        sigma = list(sigma["fragment"].values)
        if len(sigma) == 0:
            return
        timestamp = sigma[0].split('(')[1].split(')')[0].split('-')  # time stamp like str '90-120'
        timestamp = int(timestamp[-1]) - int(timestamp[0])  # time stamp like int 30

        ignore = []
        if os.path.exists(os.path.join("Z:/Tetervak/fragments", "sigma_fragments_%d_sec.csv" % timestamp)):
            ignore = pd.read_csv(os.path.join("Z:/Tetervak/fragments", "sigma_fragments_%d_sec.csv" % timestamp))
            ignore = list(ignore["fragment"].values)

        for fragment in sigma:
            if fragment not in ignore:
                ignore.append(fragment)

        ignore = pd.DataFrame({"fragment": ignore})
        ignore.to_csv(os.path.join("Z:/Tetervak/fragments", "sigma_fragments_{}_sec.csv".format(timestamp)), index=False)


    def generateFileStage(self):
        path_to_fragments = QFileDialog.getOpenFileName(self, "Choose a fragment list", "Z:/Tetervak/fragments")[0]
        if path_to_fragments == '':  # if no file selected
            return

        timestamp = int(path_to_fragments.split('_')[-2])  # time stamp like int 30

        path_to_folder = '/'.join(path_to_fragments.split('/')[:-1])
        broken_name = "broken_fragments_%d_sec.csv" % timestamp
        sigma_name = "sigma_fragments_%d_sec.csv" % timestamp

        broken = []
        if os.path.exists(os.path.join(path_to_folder, broken_name)):
            broken = list(pd.read_csv(os.path.join(path_to_folder, broken_name))["fragment"].values)

        sigma = []
        if os.path.exists(os.path.join(path_to_folder, sigma_name)):
            sigma = list(pd.read_csv(os.path.join(path_to_folder, sigma_name))["fragment"].values)

        ignore = broken + sigma
        ignore = []  # cos we don't need any ignores now

        fragments = sorted(list(pd.read_csv(path_to_fragments)["fragment"].values))
        fragments = [Fragment(fragments[i]) for i in range(len(fragments)) if fragments[i] not in ignore
                     and len(fragments[i].split('_')) == 3]

        reports = [pickle.load(open("Z:/Tetervak/Reports/reports 2.0/reports_pickle/"
                                    "{}.pickle".format(record), 'rb')) for record in self.report_list]

        for i in range(len(fragments)):
            for k in range(len(reports)):
                if reports[k].record == fragments[i].record:
                    fragments[i].ai = reports[k].getAi(fragments[i].start, fragments[i].end)
                    break

        output = {"fragment": [f.name for f in fragments if f.ai is not None],
                  "ai": [f.ai for f in fragments if f.ai is not None]}

        output = pd.DataFrame(output)
        output["ai"] = output["ai"].apply(int)
        output = output[output["ai"] > 30]
        output = output.sort_values(by="ai", ascending=False)

        now = datetime.datetime.now().strftime("%Y-%m-%d")
        path_to_save = "Z:/Tetervak/file - stage/file-stage_AI_30_sec_{}.csv".format(now)

        output.to_csv(path_to_save, index=False, columns=["fragment", "ai"], sep=';')

        print("File - stage generated")


    def allFragments(self):
        path_to_folder = QFileDialog.getExistingDirectory(self, "Choose a folder with fragments", "Z:/Lavrov")
        if path_to_folder == '':  # if no file selected
            return

        fragments = [f for f in os.listdir(path_to_folder) if os.path.isfile(os.path.join(path_to_folder, f))]

        timestamp = fragments[0].split('(')[1].split(')')[0].split('-')  # time stamp like str '90-120'
        timestamp = int(timestamp[-1]) - int(timestamp[0])  # time stamp like int 30

        path_to_save = "Z:/Tetervak/fragments"
        file_name = "All_fragments_%d_sec.csv" % timestamp

        fragments = pd.DataFrame({"fragment": fragments})
        fragments.to_csv(os.path.join(path_to_save, file_name), index=False)

        print("%s generated" % file_name)


    def updateByFileStage(self, path_to_file_stage):
        df = pd.read_csv(path_to_file_stage, delimiter=';', names=["fragment", "fixed_ai"])
        df["name_len"] = df["fragment"].apply(lambda name: len(name.split('_')))  # remove rec020_1_... fragments
        df = df[df["name_len"] == 3]
        df = df.drop(["name_len"], axis=1)
        self.correctReports(df)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CorrectionApp()
    sys.exit(app.exec_())

