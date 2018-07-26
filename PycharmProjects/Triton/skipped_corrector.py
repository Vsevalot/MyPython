import pandas as pd
import datetime
import numpy as np


def intersperse(array, item):
    result = [item] * (len(array) * 2 - 1)
    result[::2] = array
    return result


def removeRepeating(name_arr): # remove repeating from the name column
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


def findInStreak(err_df, streak=3, time_stamp=30):  # in_row parameter - the number of fragments in row which must be noted as anomaly
    records = list(err_df["error_fragment"])
    seconds = list(err_df["start_second"])
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
    final["rec"] = records
    final = final.append(pd.DataFrame.from_dict(statistic_dict), ignore_index=True)
    final["fixed_ai"] = final["expected_AI"] - round(mean_exp - mean_calc, 1)
    return final


if __name__ == "__main__":
    path_to_skipped = "Z:/Tetervak/skipped/{}"
    skipped_name = "skipped_20180716_094900.xlsx"

    df = pd.read_excel(path_to_skipped.format(skipped_name))
    df["start_second"] = df["error_fragment"].apply(matName2Time)
    df["rec"] = df["error_fragment"].apply(lambda x: x.split('_')[0])
    df = df.sort_values(["rec", "start_second"])  # sort fragments by record and these fragments by time
    df.index = [i for i in range(len(df))]

    df["streak"] = findInStreak(df)
    streak_df = df[df["streak"].notnull()]
    not_streak_df = df[df["streak"].isnull()]

    quick_fix_df = not_streak_df[not_streak_df["error"] <= 30]
    quick_fix_df.is_copy = False  # remove a SettingWithCopyWarning
    quick_fix_df["fixed_ai"] = (quick_fix_df["expected_AI"] + quick_fix_df["calculated_AI"]) / 2
    columns = ["error_fragment", "fixed_ai"]
    quick_fix_df.to_csv(path_to_skipped.format("less_30_fixed.csv"), sep=';',
                        encoding='utf-8', columns=columns, index=False)
    exit(1)

    streak_df.index = [i for i in range(len(streak_df))]
    streak_df.is_copy = False  # remove a SettingWithCopyWarning
    streak_df["time"] = streak_df["start_second"].apply(lambda x: datetime.datetime.fromtimestamp(x).time())
    streak_df["calculated_AI"] = streak_df["calculated_AI"].apply(int)
    columns = streak_df.columns.values
    split_indexes = [-1] + streak_df[streak_df["streak"] == "last"].index.tolist()  # needn't split after the last streak
    split_df = [streak_df.iloc[split_indexes[i] + 1 : split_indexes[i+1] + 1]  for i in range(len(split_indexes) - 1)]
    for i in range(len(split_df)):
        split_df[i] = addStatisctic(split_df[i])
    streak_df = pd.concat(split_df, ignore_index=True)
    streak_df.to_csv(path_to_skipped.format("more_30_streaks.csv"), sep=';', encoding='utf-8', index=False,
                     columns=["rec", "expected_AI", "calculated_AI", "time"])
    fixed_streak = streak_df[streak_df["error_fragment"].notnull()]
    fixed_streak.to_csv(path_to_skipped.format("streaks_fixed.csv"), sep=';', encoding='utf-8', index=False,
                     columns=["error_fragment", "fixed_ai"])
    big_error_df = not_streak_df[not_streak_df["error"] > 30]
    big_error_df["error_fragment"].to_csv(path_to_skipped.format("more_30_artifacts.csv"), sep=';', index=False)




