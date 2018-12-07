#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os
from array import array
from math import sqrt
import copy


MAX_LENGTH = 16000000
USHORT_MAX = 65535
SHORT_MIN = -32768
SHORT_MAX = 32767
SPS = 2120.26666666  # Samples per second MGA's recording speed
IMPEDANCE_SPIKE_LENGTH = 1.5  # Duration of an impedance measurements influence
HEADER = """File Format:1.0
Channel Count:1
#Data Type:”short”
Data Points:{}
Data:
"""

class EEG(object):
    def __init__(self, path_to_csv:str, sep:str='\t', impedance:bool=False):
        """
        Creates an EEG object from a .csv file with first column as samples of voltage (mV) and second column as
        impedance measurements status, where 1 means measurement and 0 means no measurement
        :param path_to_csv: path to a .csv file
        :param sep: which separator is used in the .csv file
        :param impedance: Set on True if there is an impedance measurement status column in the .csv file
        """
        self._name = os.path.basename(path_to_csv)[:-4]

        df = pd.read_csv(path_to_csv,
                         sep=sep,
                         names=["Voltage", "Impedance_measurement"] if impedance else ["Voltage"])
        self.eeg = df["Voltage"].values
        self.preview_eeg = self.eeg[::100]
        self.quantized_eeg = None
        self.impedance = None
        self.limits = None
        self.quality = None
        self.amplitude = None

        if impedance:
            self.impedance = df["Impedance_measurement"].values
            self.measure_samples = []
            for i in range(len(self.impedance)):
                if self.impedance[i] == 1:
                    if self.impedance[i - 1] == 0:
                        self.measure_samples.append(i)  # append number of a sample where a measurement began
            if self.measure_samples[0] == 0:
                self.measure_samples = self.measure_samples[1:]


    def __repr__(self):
        return "{self.__class__.__name__} from {self._name}".format(self=self)

    def quantize_eeg(self, first_sample: int = 0, length: int = -1, diapason_width: float = 0.01):
        """
        Quantize self.no_imp_eeg from Volt float point values between -32768 and 32767 (Short data type)
        :param first_sample: staring sample if only a part of an eeg signal needed
        :param length: length of the chosen part, if not specified all signal or 1.6e7 points from the middle of the
        signal would be used
        :param diapason_width: All values lower of higher from half of this parameter would be equated to cup level.
        Note that the bigger this parameter is, the bigger
        quantization step is (for (-0.5:0,5)mV one step is about 15 nV).
        Function will try to find the most effective shift for this diapason to maximise valuable information.
        :return:
        """
        if length == -1:  # if length of the fragment to quantize is not specified
            new_length = len(self.no_imp_eeg)
            if new_length > MAX_LENGTH:  # picking the central part of a signal quantized
                excess = new_length - MAX_LENGTH
                shift = int(excess / 2)
                self.measure_samples = [sample - shift for sample in self.measure_samples
                                        if sample - shift > 1 and sample - shift > MAX_LENGTH]
                return self.quantize_eeg(shift, MAX_LENGTH, diapason_width)  # use central part of the signal
            else:
                return self.quantize_eeg(0, len(self.no_imp_eeg), diapason_width)  # use the whole signal

        if length < 1000 or length > MAX_LENGTH:
            print("Wrong length of the signal, it must has between 1000 and 1.6e7 points")
            exit(-1)

        eeg = copy.deepcopy(self.no_imp_eeg[first_sample: first_sample + length])
        eeg -= np.mean(eeg)  # central signal to zero

        borders = [-diapason_width / 2, diapason_width / 2]
        self.limits = tuple(borders)
        self.amplitude = diapason_width

        #  Cutting voltage values which overlap borders
        for i in range(len(eeg)):
            if eeg[i] < borders[0]:
                eeg[i] = borders[0]
            elif eeg[i] > borders[1]:
                eeg[i] = borders[1]

        eeg -= borders[0]  # lifting signal up to 0 to convert it to unsigned short

        short_arr = array("h")  # h = signed short, H = unsigned short
        step = (borders[1] - borders[0]) / USHORT_MAX
        for i in range(len(eeg)):
            short_arr.append(int(eeg[i] / step) + SHORT_MIN)

        self.quantized_eeg = short_arr
        unquantized_eeg = np.array(list(self.quantized_eeg))
        unquantized_eeg -= SHORT_MIN
        unquantized_eeg = np.array([i * step for i in unquantized_eeg])
        error = .0
        # for i in range(len(unquantized_eeg)):
        #     error += (eeg[i + first_sample] - unquantized_eeg[i]) ** 2
        # print("Error = %f" % error)
        self.sigma = sqrt(error / len(unquantized_eeg)) / (len(unquantized_eeg) - 1)
        self.quantization_step = diapason_width  * 10**6 / (SHORT_MAX - SHORT_MIN)

        cut_eeg = 0  # This value is needed to calculate % of changed eeg and assess amount of lost information
        for i in range(len(short_arr)):
            if short_arr[i] == SHORT_MIN or short_arr[i] == SHORT_MAX:
                cut_eeg += 1
        self.quality = 100 - 100 * cut_eeg / len(short_arr)


    def add_no_impedance(self, impedance_spike_duration=1.7, smoothing_length=20):
        """
        Uses data from self.eeg and self.measure_samples and add self.no_imp_eeg (signal without impedance)
        and inserts last N samples before a spike for each impedance measurement caused spike in an eeg signal,
        N calculates as SPS * duration of spike
        :param impedance_spike_duration: Duration of time period (seconds) where an impedance measurement influences on EEG
        :param smoothing_length: Number of samples which would be given to a moving average filter
        :return: None
        """
        if self.impedance is None:
            print("Use .csv file with column for impedance measurements status and pass argument impedance=True while"
                  "generating EEG instance")
            return

        spike_length = int(impedance_spike_duration * SPS)  # length of a spike caused by impedance measurements
        no_imp_eeg = []

        if len(self.measure_samples) == 0:
            self.no_imp_eeg = self.eeg
            return

        for i in range(len(self.measure_samples)):  # for each spike
            if self.measure_samples[i] > len(self.eeg):
                print("Wrong sample number. "
                      "Expected number less than {} got {} instead".format(len(self.eeg),
                                                                           self.measure_samples[i]))
                exit(-1)

            spike_beginning = self.measure_samples[i]
            spike_end = self.measure_samples[i] + spike_length

            if self.measure_samples[i] < spike_length:  # at the start
                # if first spike is in less than one spike duration from the beginning
                # take all samples before the first spike
                no_imp_eeg = np.append(no_imp_eeg, [self.eeg[: spike_beginning]])
                k = 0
                instead_of_spike = []
                # use all signal from the beginning to the beginning of impedance measurements several times
                while k < spike_length:
                    instead_of_spike.append(self.eeg[k % spike_beginning])
                    k += 1
                no_imp_eeg = np.append(no_imp_eeg, [instead_of_spike])
            else:
                # add all points between spikes
                if i == 0:
                    no_imp_eeg = np.append(no_imp_eeg, [self.eeg[:spike_beginning]])
                else:
                    no_imp_eeg = np.append(no_imp_eeg,
                                           [self.eeg[self.measure_samples[i - 1] + spike_length: spike_beginning]])

                if spike_end > len(self.eeg):  # at the end
                    # Else if a spike duration is larger than the signal lasts - insert last N samples
                    # before the spike to it place
                    no_imp_eeg = np.append(no_imp_eeg, [self.eeg[-(spike_end - len(self.eeg)):]])
                else:  # if a spike is at the middle of the signal
                    no_imp_eeg = np.append(no_imp_eeg, [self.eeg[spike_beginning - spike_length: spike_beginning]])

        if len(no_imp_eeg) < len(self.eeg):
            no_imp_eeg = np.append(no_imp_eeg, [self.eeg[self.measure_samples[-1] + spike_length:]])
        self.no_imp_eeg = no_imp_eeg

    def save2arb(self, path_to_folder):
        with open("%s/%s_%fVpp.arb" % (path_to_folder, self._name[:6], self.amplitude), 'w') as file:
            file.write(HEADER.format(len(self.quantized_eeg)))
            for v in self.quantized_eeg:
                file.write("{}\n".format(v))
            file.close()


if __name__ == "__main__":
    path_to_csv = "Z:/Tetervak/rec5xx/500/rec500_20140224_11.49.50.csv"
    if path_to_csv == "":
        print("Set a valid path to a csv with EEG + Impedance measurement")
        exit(0)
    path_to_folder = ""
    for i in range(len(path_to_csv) - 1, -1, -1):
        if path_to_csv[i] == '\\' or path_to_csv[i] == '/':
            path_to_folder = path_to_csv[:i]
            break

    eeg = EEG(path_to_csv, impedance=True)
    eeg.add_no_impedance()  # add eeg without impedance
    diapasons = [0.01, 0.05, 0.1, 0.5]  # Width of quantize window in Volts. Add additional value if needed
    for width in diapasons:
        eeg.quantize_eeg(diapason_width=width)
        eeg.save2arb(path_to_folder)

        f = plt.figure(figsize=(16.0, 12.0))  # draw graphs
        axes = f.add_subplot(3, 1, 1)
        axes.plot(np.arange(len(eeg.eeg)), eeg.eeg - np.mean(eeg.eeg))  # Pure eeg
        for spike in eeg.measure_samples:
            axes.axvline(x=spike, color = 'red', linestyle='--', alpha=.3)
        axes.set_title("%s - Raw eeg" % eeg._name)
        axes = f.add_subplot(3, 1, 2)
        axes.plot(np.arange(len(eeg.no_imp_eeg)), eeg.no_imp_eeg)  # eeg without impedance measurements
        for spike in eeg.measure_samples:
            axes.axvline(x=spike, color = 'red', linestyle='--', alpha=.3)
        axes.set_title("%s - Removed impedance eeg" % eeg._name)
        axes = f.add_subplot(3, 1 ,3)
        axes.plot(np.arange(len(eeg.quantized_eeg)), eeg.quantized_eeg)  # Quantized eeg
        for spike in eeg.measure_samples:
            axes.axvline(x=spike, color = 'red', linestyle='--', alpha=.3)
        axes.set_title("%s - Quantized eeg" % eeg._name)
        plt.savefig("%s/%s_%fVpp_%.1f %c.jpg" % (path_to_folder, eeg._name[:6], eeg.amplitude, eeg.quality, '%'))
        print("%s complete,quantization step = %f mkV, quality = %.1f %c" %
              (eeg._name, eeg.quantization_step, eeg.quality, '%'))
