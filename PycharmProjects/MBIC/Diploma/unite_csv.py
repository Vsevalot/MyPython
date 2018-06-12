#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

if __name__ == "__main__":
    path_to_eeg = "Global indexes.csv"
    path_to_acc = "Acce features.csv"

    eeg_df = pd.read_csv(filepath_or_buffer=path_to_eeg, sep=';', encoding="ISO-8859-1")
    print(eeg_df.shape)
    acc_df = pd.read_csv(filepath_or_buffer=path_to_acc, sep=';', encoding="ISO-8859-1")
    print(acc_df.shape)


    for column in acc_df:
        eeg_df[column] = acc_df[column]

    df = eeg_df
    df = df.drop(['ubject'], axis=1)

    df.dropna(how="all", inplace=True)  # drops the empty line at file-end




