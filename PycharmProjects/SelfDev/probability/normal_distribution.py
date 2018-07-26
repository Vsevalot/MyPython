#!/usr/bin/python3
# -*- coding: utf-8 -*-
from math import sqrt, e, pi
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt


def normal_pdf(x, mu=0, sigma_squared=1):
    numerator =  sqrt(2 * pi * sigma_squared)
    denominator = e **-(((x - mu)**2) / (2 * sigma_squared))
    return  denominator / numerator


def normalProbabilityDensity(x):
    constant = 1.0 / np.sqrt(2*np.pi)
    return(constant * np.exp((-x**2) / 2.0) )


if __name__ == "__main__":
    mu = 0
    sigma = 1
    sigma_squared = sigma**2
    x = np.linspace(mu - sigma * 4, mu + sigma * 4, 1000)
    y = np.array([normalProbabilityDensity(point) for point in x])
    sigma1 = []
    sigma2 = []
    sigma3 = []

    for i in range(len(x)):
        if x[i] > mu - 3 * sigma and x[i] < mu + 3 * sigma:
            sigma3.append(y[i])
            if x[i] > mu - 2 * sigma and x[i] < mu + 2 * sigma:
                sigma2.append(y[i])
                if x[i] > mu - sigma and x[i] < mu + sigma:
                    sigma1.append(y[i])


    coefficient = 1 / sum(y)
    print(coefficient * sum(sigma1), coefficient * sum(sigma2), coefficient * sum(sigma3))

    print(quad(normalProbabilityDensity, -1, 1))
    print(quad(normalProbabilityDensity, -2, 2))
    print(quad(normalProbabilityDensity, -3, 3))


    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x, y)
    ax.axvline(x=mu - 3 * sigma, color='r')
    ax.axvline(x=mu + 3 * sigma, color='r')
    ax.axvline(x=mu - 2 * sigma, color='y')
    ax.axvline(x=mu + 2 * sigma, color='y')
    ax.axvline(x=mu - sigma, color='g')
    ax.axvline(x=mu + sigma, color='g')
    plt.show()
