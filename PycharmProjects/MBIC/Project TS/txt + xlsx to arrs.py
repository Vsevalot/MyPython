import os
import pandas as pd
from scipy.signal import butter, lfilter
from numpy import mean, std, fft


def threeSigma(list):
    sigma = 3*std(list)
    return [v if abs(v)<sigma else sigma if v>0 else -sigma for v in list]

def ecg2hrv(ecg):
    hrv_t = [0]
    min_v = abs(min(ecg))
    up_ecg = [v + min_v for v in ecg]
    threshold = mean(up_ecg) + std(up_ecg)
    i = 0
    while i<len(up_ecg):
        if up_ecg[i]>threshold:
            hrv_t.append(i*4)
            i+=125
        i+=1

    hrv = [hrv_t[i+1] - hrv_t[i] for i in range(len(hrv_t) - 1)]
    nn50 = len([i for i in range((len(hrv)-1)) if abs(hrv[i]-hrv[i+1])>50])
    pnn50 = nn50/len(hrv)
    print(nn50, pnn50)
    from scipy.interpolate import interp1d
    import numpy as np
    new_time = np.linspace(0, hrv_t[-1], len(ecg))
    x = np.array(hrv_t[:])
    y = np.array(hrv+[hrv[-1]])
    return interp1d(x, y)(new_time)

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
    procedure_dict = {columns[i]: threeSigma(lines[i]) for i in range(len(lines))}

    procedure_dict["HRV"] = ecg2hrv(procedure_dict["ECG"])
    procedure_dict.pop("Time", None)
    procedure_dict.pop("ECG", None)


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

    sum_power = 0
    for stage in data_dict[patient]:
        for procedure in ['Theta', 'Alpha', 'BetaL', 'BetaH', "PPG", "EDA", "HRV"]:
            if procedure in ['Theta', 'Alpha', 'BetaL', 'BetaH']:
                data_dict[patient][stage][procedure] = round(sum(abs(fft.fft(data_dict[patient][stage][procedure]))),3)
                sum_power+=data_dict[patient][stage][procedure]
            elif procedure in ["PPG", "EDA"]:
                m = max([max(data_dict[patient][stage][procedure]),
                         abs(min(data_dict[patient][stage][procedure]))]) # normalizing
                data_dict[patient][stage][procedure] = [v/m for v in data_dict[patient][stage][procedure]]
                data_dict[patient][stage][procedure + "_mean"] = mean(data_dict[patient][stage][procedure])
                data_dict[patient][stage][procedure + "_std"] = std(data_dict[patient][stage][procedure])
                data_dict[patient][stage].pop(procedure, None)
            elif procedure == "HRV":
                import math
                hrv = list(data_dict[patient][stage][procedure])
                data_dict[patient][stage]["HRV_mean"] = mean(hrv)
                data_dict[patient][stage]["HRV_std"] = std(hrv)
                data_dict[patient][stage]["HRV_rmssd"] = math.sqrt(sum([(hrv[i] - hrv[i+1])**2
                                                                        for i in range(len(hrv)-1)])/ len(hrv))
                data_dict[patient][stage]["HRV_cv"] =100*data_dict[patient][stage]["HRV_std"]/data_dict[patient][stage]["HRV_mean"]

                data_dict[patient][stage]["HF"] = butter_bandpass_filter(data_dict[patient][stage][procedure], 0.4, 0.15, 250)
                data_dict[patient][stage]["LF"] = butter_bandpass_filter(data_dict[patient][stage][procedure], 0.15, 0.04, 250)
                data_dict[patient][stage]["VLF"] = butter_bandpass_filter(data_dict[patient][stage][procedure], 0.04, 0.003, 250)

                data_dict[patient][stage]["HF"] = round(sum(abs(fft.fft(data_dict[patient][stage]["HF"])))/len(hrv),3)
                data_dict[patient][stage]["LF"] = round(sum(abs(fft.fft(data_dict[patient][stage]["LF"])))/len(hrv),3)
                data_dict[patient][stage]["VLF"] = round(sum(abs(fft.fft(data_dict[patient][stage]["VLF"])))/len(hrv),3)

                data_dict[patient][stage]["HF/LF"] = data_dict[patient][stage]["HF"]/data_dict[patient][stage]["LF"]

                data_dict[patient][stage].pop(procedure, None)

    for stage in data_dict[patient]:
        for procedure in ['Theta', 'Alpha', 'BetaL', 'BetaH']:
            data_dict[patient][stage][procedure] = data_dict[patient][stage][procedure]/sum_power

path_to_save = "pandas.csv"
components = ["HRV_mean","HRV_std", "HRV_rmssd","HRV_cv","PPG_mean", "HF", "LF", "VLF", "HF/LF",
              "PPG_std", "EDA_mean", "EDA_std", 'Theta', 'Alpha', 'BetaL', 'BetaH']
with open(path_to_save, 'w') as file:
    line = ';'.join(components) + ";Stage\n"
    file.write(line)

    for patient in data_dict:
        for stage in data_dict[patient]:
            line = ""
            for component in components:
                line+="{};".format(data_dict[patient][stage][component] if data_dict[patient][stage][component] is not None else 1)
            line+=stage+'\n'
            file.write(line)



