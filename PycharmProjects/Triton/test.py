#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import datetime

if __name__ == "__main__":
    start = time.time()
    start_502 = datetime.datetime(year=2014, month=2, day=26,hour=9, minute=1, second=47)
    while(1):
        time.sleep(10)
        diff = time.time() - start
        from_start = datetime.datetime.fromtimestamp(start_502.timestamp() + diff)
        print(from_start.time())

