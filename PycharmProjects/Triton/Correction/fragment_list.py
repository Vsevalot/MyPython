#!/usr/bin/env python3

import pandas as pd
import os


if __name__ == "__main__":
    path_to_folder = ""
    fragments = [f for f in os.listdir(path_to_folder) if os.path.isfile(os.path.join(path_to_folder, f))]

    timestamp = fragments[0].split('(')[1].split(')')[0]  # time stamp like str '90-120'
    timestamp = int(timestamp[-1]) - int(timestamp[0])  # time stamp like int 30

    path_to_save = "Z:/Tetervak/fragments"
    file_name = "All_fragments_%d_sec.csv" % timestamp

    fragments = pd.DataFrame({"fragment": fragments})
    fragments.to_csv(os.path.join(path_to_save, file_name))