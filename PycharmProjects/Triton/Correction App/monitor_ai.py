#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import pandas as pd
import numpy as np


def time_to_seconds(time:float)->int:
    """
    Converts time from HH.MM to seconds from 00:00
    :param time: Because 9.13 is read as float use float param
    :return: number of seconds since 00:00
    """
    hour, minute = str(time).split('.')
    return int(hour) * 3600 + (int(minute) * 60 if len(minute) == 2 else int(minute) * 600)  # cos 9.20 reads as 9.2


def moving_average(signal, point, wide = 11):
    """
    Moving average function for smoothing edge between two signals
    :param signal: list of values
    :param point: edge - centre of a location which must be smoothed
    :param wide: number of samples which would be used to calculate average value
    :return: Smoothed signal
    """
    if point - 2 * wide < 0:
        print("The edge is too close to the beginning of the signal for smoothing")
        exit(-1)
    elif point + 2 * wide > len(signal):
        print("The signal is too small for smoothing")
        exit(-1)

    smoothed = []
    for i in range(point - 2* wide, point + wide):
        smoothed.append(int(sum(signal[i: i + wide]) / wide))

    signal[point - 2 * wide: point + wide] = smoothed  # replace points with smoothed


if __name__ == "__main__":
    path_to_ai = "Z:/Tetervak/Reports/reports 2.0/monitor_ai"
    ais = {rec: pd.read_csv(os.path.join(path_to_ai, rec), delimiter=';') for rec in os.listdir(path_to_ai) if
           len(rec) == 7 and rec[-3:] == "csv"}  # len(ai) == 7 to avoid bad AI
    for rec in ais:
        name = rec[:-4]
        ai = ais[rec]["monitor_ai"].values
        times = ais[rec]["time"].values
        times = np.array([time_to_seconds(t) for t in times])
        times -= times[0]

        ai_column = []

        for i in range(1, len(times), 1):
            for k in range(times[i]):
                ai_column.append(ai[i - 1])

        for k in range(2 * 60):  # add two minutes with the last ai value to the end of a file
            ai_column.append(ai[-1])


        for i in range(1, len(times), 1):
            moving_average(ai_column, times[i])


        with open("Z:/Tetervak/Reports/reports 2.0/monitor_ai/%s.txt" % rec.split('.')[0], 'w') as file:
            for i in range(len(ai_column)):
                file.write("%d\n" % ai_column[i])
            file.close()
    print("Complete")
