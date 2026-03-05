import pandas as pd
import numpy as np


def country_ifr(params, population_yearly) -> pd.Series:
    h = (
        lambda x: x / 2
        - 1 / (2 * params[2]) * np.log(np.cosh(params[2] * (x - params[3])))
        + 1 / (2 * params[2]) * np.log(np.cosh(params[2] * (-params[3])))
    )
    f = lambda x: np.exp(params[0] * h(x) + params[1])
    age = np.arange(100)
    mortality_curve = f(age)
    return population_yearly.apply(lambda x: mortality_curve * x).sum(
        axis=0
    ) / population_yearly.sum(axis=0)


def mortality_curve(params):
    h = (
        lambda x: x / 2
        - 1 / (2 * params[2]) * np.log(np.cosh(params[2] * (x - params[3])))
        + 1 / (2 * params[2]) * np.log(np.cosh(params[2] * (-params[3])))
    )
    f = lambda x: np.exp(params[0] * h(x) + params[1])

    age = np.arange(100)
    mortality_curve = f(age)
    return mortality_curve
