#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
#
# a = "<p><b>Tproger</b> — мой <i>любимый</i> сайт о программировании!</p>"
#
# print(re.findall(r"<.*>", a))
# print(re.findall(r"<[^>]*>", a))
# print(re.findall(r"<.*?>", a))
# print(re.findall(r"<(.*?)>", a))

a = ["1.2 *3.4", "1 + 2", "-3/ -6", "-2-2"]

for i in a:
    print(re.findall(r"(-?\d+(?:\.\d+)?)\s*([-+*\/])\s*(-?\d+(?:\.\d+)?)", i))
    print(re.findall(r"-?\d+(\.\d+)?", i))

