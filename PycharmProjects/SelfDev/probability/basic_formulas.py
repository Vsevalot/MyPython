from functools import reduce
from math import e


def factorial(n):
    if n < 0:
        print("n must be > 0!")
        exit(33)
    elif type(n) != int:
        print("n must be an integer")
        exit(33)
    else:
        if n == 1 or n == 0:
            return 1
        return reduce(lambda a, b: a * b, [i + 1 for i in range(n)])  # just factorial


def cumulative(n, p, x):
    return sum([probability(n, p, i) for i in range(x + 1)])


def probability(n, p, x):
    return combination(n, x) * p**x * (1 - p) ** (n - x)


def combination(n, x):
    numerator = [i + n - x for i in range(x + 1)]
    numerator[0] = 1  # to calculate multiplication of all elements correct not 0
    numerator = reduce(lambda a, b: a * b, numerator)
    denominator = factorial(x)
    return int(numerator / denominator)


def poisson_prob(lmd, k):
    return lmd**k * e**-lmd / factorial(k)
