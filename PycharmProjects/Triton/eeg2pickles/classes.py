import pickle
import pandas as pd
import numpy as np


class eeg(object):
    def __init__(self, path_to_csv):
        eeg = pd.read_csv(path_to_csv, names=["voltage"])["voltage"].values