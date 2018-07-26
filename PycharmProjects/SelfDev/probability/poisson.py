#!/usr/bin/python3
# -*- coding: utf-8 -*-
from math import sqrt
from functools import reduce
import matplotlib.pyplot as plt
from basic_formulas import poisson_prob


if __name__ == "__main__":
    lmd = 3.9
    k = 9
    probabilities = [poisson_prob(lmd, i) for i in range(k + 1)]
    less_k = sum(probabilities[:-1])
    k_and_more = 1 - less_k
    print("With lambda = %d" % lmd)
    print("The probability of {} is {} %".format(k, round(probabilities[k] * 100, 5)))
    print("The probability of less than {} is {} %".format(k, round(less_k * 100, 5)))
    print("The probability of {} and more is {} %".format(k, round(k_and_more * 100, 5)))

