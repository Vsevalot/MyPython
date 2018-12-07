#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from reportlib import Fragment, ReportAI


if __name__ == "__main__":
    path_to_reports = "Z:/Tetervak//Reports/reports 2.0/reports_csv"
    reports = [os.path.join(path_to_reports, r) for r in os.listdir(path_to_reports)]
    reports = [ReportAI(r) for r in reports]

    for r in reports:
        r.saveToPickle()