#!/usr/bin/python3
# -*- coding: utf-8 -*-


if __name__ == "__main__":
    numbers = {'0': "abcdef",
               '1': "bc",
               '2': "abged",
               '3': "abgcd",
               '4': "fgbc",
               '5': "afgcd",
               '6': "afgcde",
               '7': "abc",
               '8': "abcdefg",
               '9': "abcdfg"}

    numbers = {n: {"high": numbers[n], "low": [c for c in "abcdefg" if c not in numbers[n]]} for n in numbers}

    for i in numbers:
        print(i, numbers[i])
