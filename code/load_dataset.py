import pandas as pd
import numpy as np


def load_population(from_year=2015, to_year=2021) -> pd.DataFrame:
    population = pd.read_csv("../data/Population.csv").loc[
        :, ["geo", "TIME_PERIOD", "OBS_VALUE", "sex", "age"]
    ]
    population.columns = ["Country", "Year", "Value", "Sex", "Age group"]
    conditions = np.logical_and(
        population["Year"] >= from_year, population["Year"] <= to_year
    )
    conditions = np.logical_and(conditions, population["Sex"] == "T:Total")
    population = population[conditions].drop(columns=["Sex"])
    population.loc[:, "Country"] = population["Country"].apply(
        lambda x: x.split(":")[1]
    )
    population.loc[:, "Age group"] = population["Age group"].apply(
        lambda x: x.split(":")[1].split(" ")[0]
    )
    population.loc[:, "Age group"] = population["Age group"].apply(
        lambda x: 0 if x == "Less" else x
    )
    population = population[~population["Age group"].isin(["Unknown", "Open-ended"])]
    population = population[
        ~population["Country"].isin(
            [
                "Euro area - 18 countries (2014)",
                "Euro area - 19 countries  (2015-2022)",
                "European Free Trade Association",
                "European Union - 27 countries (from 2020)",
                "Germany including former GDR",
            ]
        )
    ]
    population.loc[:, "Country"] = population["Country"].replace(
        {"Germany (until 1990 former territory of the FRG)": "Germany"}
    )

    population_yearly = population[population["Year"] == 2019]
    population_yearly = population_yearly[
        ~population_yearly["Age group"].isin(["Total"])
    ]
    population_yearly.loc[:, "Age group"] = population_yearly["Age group"].apply(
        lambda x: int(x)
    )
    population_yearly = population_yearly.pivot(
        index="Country", columns="Age group", values="Value"
    ).fillna(0)

    population = population[population["Age group"] == "Total"]
    population = population.pivot(
        index="Country", columns="Year", values="Value"
    ).fillna(0)
    population.loc["United Kingdom", 2020] = population.loc["United Kingdom", 2019]
    population.loc["United Kingdom", 2021] = population.loc["United Kingdom", 2019]
    return population_yearly, population


def load_covid_deaths() -> pd.DataFrame:
    covid_deaths = pd.read_csv("../data/JHUCovidDeaths.csv")
    return covid_deaths.pivot(index="Country", columns="Date", values="Deaths").fillna(
        0
    )


def load_deaths():
    deaths = pd.read_csv("../data/Deaths.csv").loc[
        :, ["geo", "TIME_PERIOD", "OBS_VALUE", "sex", "age"]
    ]
    deaths.columns = ["Country", "Week", "Value", "Sex", "Age group"]
    condition = np.logical_and(deaths["Week"] >= "2015-W01", deaths["Sex"] == "T:Total")
    condition = np.logical_and(condition, deaths["Age group"] == "TOTAL:Total")
    deaths = deaths[condition]
    deaths = deaths[deaths["Country"].apply(lambda x: len(x.split(":")[0])) == 2]
    deaths.loc[:, "Country"] = deaths["Country"].apply(lambda x: x.split(":")[1])
    deaths.loc[:, "Country"] = deaths.loc[:, "Country"].replace(
        {"Germany (until 1990 former territory of the FRG)": "Germany"}
    )
    df = deaths["Week"].str.split("-", expand=True)
    df.columns = ["Year", "Week"]
    deaths.loc[:, ["Year", "Week"]] = df
    deaths = (
        deaths.pivot(index=["Year", "Country"], columns="Week", values="Value")
        .fillna(0)
        .drop(columns=["W99"])
    )

    deathsUK = pd.read_csv("../data/UKDeaths2021.csv").pivot(
        index="Year", columns="Week", values="Deaths"
    )
    deaths.loc[("2021", "United Kingdom"), deathsUK.columns] = deathsUK.values

    deaths.loc[("2015", "North Macedonia"), :] = 0
    deaths.loc[("2016", "North Macedonia"), :] = 0
    deaths.loc[("2017", "North Macedonia"), :] = 0
    deaths.loc[("2018", "North Macedonia"), :] = 0
    deaths.loc[("2019", "North Macedonia"), :] = 0
    deaths.loc[("2020", "North Macedonia"), :] = 0
    deaths.loc[("2021", "North Macedonia"), :] = 0
    deaths.loc[("2022", "North Macedonia"), :] = 0
    deaths.loc[("2023", "North Macedonia"), :] = 0
    return deaths
