import os
import pandas as pd
from scipy.signal import butter, lfilter
from numpy import mean, std, fft


def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq

    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y

def txt_to_list(path_to_txt):
    lines = []
    with open(path_to_txt, 'r') as file:
        data = False
        for line in file:
            if line[:2] == "0\t":
                data = True
            if data:
                doted = line.replace(',','.')
                float_line = [float(v) for v in doted.split('\t')]
                float_line[0] = int(float_line[0])
                lines.append(float_line)

    lines = [[lines[k][i] for k in range(len(lines))] for i in range(len(lines[0]))] # transposing
    EEG = {'Theta': list(butter_bandpass_filter(lines[4], 4, 7, 250)),
           'Alpha': list(butter_bandpass_filter(lines[4], 7, 15, 250)),
           'BetaL': list(butter_bandpass_filter(lines[4], 15, 25, 250)),
           'BetaH': list(butter_bandpass_filter(lines[4], 25, 31, 250))}

    del lines[3] # second PPG
    del lines[3] # pure EEG


    columns = ['Time', 'ECG', 'PPG', 'EDA']
    procedure_dict = {columns[i]: lines[i] for i in range(len(lines))}

    procedure_dict.pop("ECG", None)
    procedure_dict.pop("Time", None)

    for rhythm in EEG:
        procedure_dict[rhythm] = EEG[rhythm]
    return procedure_dict

path_to_data = "data"
txt_names = [os.path.join(path_to_data, f) for f in os.listdir(path_to_data) if
                        os.path.isfile(os.path.join(path_to_data, f))]

data_dict = {txt.split('\\')[-1].split('.')[0]: txt_to_list(txt) for txt in txt_names}


path_to_book = "Stages.xlsx"
df_skipped = pd.read_excel(path_to_book, header=None)

stages = {"VV":[v*250 for v in [0, 120,250,376,505]],
          "MAV": [v*250 for v in [0, 120, 257, 394, 520]],
          "RM": [v*250 for v in [0, 120, 256, 394, 514]],
          "DK": [v*250 for v in [0, 120, 250, 382, 504]],
          "KEI": [v*250 for v in [0, 120, 257, 386, 506]]
          }

stage_names = ["Background", "Cognitive", "Emotional", "Afterwards"]

for patient in data_dict: # some python magic
    data_dict[patient] = {stage_names[k]: {procedure: data_dict[patient][procedure][stages[patient][k]: stages[patient][k+1]] for procedure in data_dict[patient]} for k in range(len(stage_names))}

    for stage in data_dict[patient]:
        for procedure in data_dict[patient][stage]:
            if procedure in ['Theta', 'Alpha', 'BetaL', 'BetaH']:
                data_dict[patient][stage][procedure] = round(sum(abs(fft.fft(data_dict[patient][stage][procedure]))),3)
            else:
                data_dict[patient][stage][procedure] = {"mean": mean(data_dict[patient][stage][procedure]),
                                                        "std": std(data_dict[patient][stage][procedure])}



print(1)


