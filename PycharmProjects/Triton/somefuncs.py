import pandas as pd
import datetime
import numpy
import os

def justName(matfile_name: str) -> str:
    return matfile_name.split('_')[0][1:]

def matName2Time(matfile_name: str) -> [datetime.datetime, int]:  # convert Mat file's name to date and time
    if type(matfile_name) == float:
        return numpy.nan
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

def compareRows(err_df, path_to_save = "E:\\test", in_row = 3):
    records = list(err_df["error_fragments"])
    seconds = list(err_df["start_second"])
    diff = in_row - 1
    closest = [False for rec in records]
    non_artefacts = []
    i = 0
    while i < len(records) - diff:
        if records[i].split('_')[0][1:] == records[i+diff].split('_')[0][1:]:
            if seconds[i] >= seconds[i + diff] - diff*30:
                closest[i] = True
                i += 1
                non_artefacts.append([records[i].split('_')[0][1:], datetime.datetime.fromtimestamp(seconds[i]).time()])
                while seconds[i] - seconds[i-1] <= 30:
                    closest[i] = True
                    i += 1
                non_artefacts[-1].append(datetime.datetime.fromtimestamp(seconds[i]).time())
                continue
        i += 1

    with open(os.path.join(path_to_save, "more_than_30.csv"), 'w') as file:
        for anomaly in non_artefacts:
            file.write("{};{}-{}\n".format(anomaly[0], anomaly[1], anomaly[2]))
        file.close()


    return err_df[closest], err_df[[not v for v in closest]]



if __name__ == "__main__":
    path_to_skipped = "E:\\test\\approx_bisp_ws_20180516_180400.xlsx"
    df = pd.read_excel(path_to_skipped, header=None)
    df_columns = ["broken_fragments", "broken_comment", "sigma_fragments", "sigma_comment", "error_fragments",
                  "report_stage", "report_ai", "classifier_ai", "error_value"]
    df.columns = df_columns

    df["start_second"] = df["error_fragments"].apply(matName2Time)

    #df.error_fragments = df.error_fragments.apply(justName) # convert time intervals to seconds

    broken_df = df[["broken_fragments", "broken_comment"]]
    sigma_df = df[["sigma_fragments", "sigma_comment"]]

    error_df = df[["error_fragments", "start_second", "report_ai", "classifier_ai", "error_value"]]
    quick_fix_df = error_df[error_df.error_value <= 30]
    quick_fix_df["average"] = (quick_fix_df.report_ai + quick_fix_df.classifier_ai)/2
    big_error_df =  error_df[error_df.error_value > 30]
    big_error_df = big_error_df.sort_values(["error_fragments", "start_second"])

    in_row_df, not_row_df = compareRows(big_error_df)

    not_row_df["error_fragments"].to_csv("E:\\test\\more_than_30_artifacts.csv", sep = ';', index = False)


