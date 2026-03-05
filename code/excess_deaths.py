import pandas as pd


def calculate_max_deaths(deaths, population):
    deaths_correction = _deaths_correction(population, 2020)
    deaths_correction = deaths_correction.dropna(axis=0)
    max_deaths_2020 = (
        deaths.copy()
        .apply(lambda x: x / deaths_correction.loc[x.name[1], int(x.name[0])], axis=1)
        .reset_index()
        .groupby("Country")
        .max()
        .drop(columns=["Year"])
    )
    max_deaths_2020 = max_deaths_2020.add_prefix("2020")

    deaths_correction = _deaths_correction(population, 2021)
    deaths_correction = deaths_correction.dropna(axis=0)
    max_deaths_2021 = (
        deaths.copy()
        .apply(lambda x: x / deaths_correction.loc[x.name[1], int(x.name[0])], axis=1)
        .reset_index()
        .groupby("Country")
        .max()
        .drop(columns=["Year"])
    )
    max_deaths_2021 = max_deaths_2021.add_prefix("2021")

    return pd.concat([max_deaths_2020, max_deaths_2021], axis=1)


def _deaths_correction(population, year):
    deaths_correction = population.copy()
    deaths_correction = deaths_correction.apply(lambda x: x / x.loc[year], axis=1)
    return deaths_correction
