#!/usr/bin/python3
# -*- coding: utf-8 -*-
from math import sqrt
from functools import reduce
import matplotlib.pyplot as plt
from basic_formulas import probability


if __name__ == "__main__":
    p = 1 / 12
    n = 250
    probabilities = [probability(n, p, i) for i in range(n + 1)]
    mu = p * n
    std = sqrt((1 - p) * mu)
    x = 30
    prob_x = probabilities[x]
    x_and_more = sum(probabilities[x:]) if x > len(probabilities) / 2 else 1 - sum(probabilities[:x])
    print("Mu = %.3f" % mu)
    print("Sigma = %.3f" % std)
    print("The probability of {} is {}%".format(x, prob_x * 100))
    print("The probability that {} and more is {} %".format(x, round(x_and_more * 100, 5)))



    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.bar([x for x in range(n + 1)], probabilities)
    plt.show()
