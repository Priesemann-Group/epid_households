# Households in epidemic disease spread

Supplementary code for our manuscript [**Household size can explain 40% of the variance in cumulative COVID-19 incidence across Europe**](https://arxiv.org/abs/2602.15447) publication.

License: [GPL v3](https://www.gnu.org/licenses/gpl-3.0)



## Usage

Clone the repository with

```bash
git clone git@https://github.com/Priesemann-Group/epid_households
```

There are many ways to install the python packages specified in requirements.txt.
We suggest a virtual environment on Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name=.venv
```

The last command builds a kernel that can be used in the Jupyter notebooks, make sure it is selected after starting Jupyter.


## Demo

A small demo can be found in ./notebooks/demo.ipynb.

This demo runs the main functions with 50 instead of ~50000 bootstraping samples.

Download the required death [data](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/DEMO_R_MWK2_05/?format=SDMX-CSV&lang=en&label=both) and save it to ./data/Deaths.csv

Execution of the demo should run within minutes on a normal desktop PC; however, systems with less than 16 GB of RAM may experience swapping.

**Disclamer: Running the bootstrap with 50 instead of 50000 samples generates unprecise results and is only meant for demo/testing purposes.**



## Plotting

The figures in ./figures/ can be reproduced with the following notebooks:

| Figure | Title | Notebook |
| ------ | ----- | ---------|
| 1 (B)  | Disease spread from the perspective of households. | [figure_1b](./notebooks/figure_1b.ipynb) |
| 2      | Differences in the effective household size can explain about 40% of the variation in COVID-19 prevalence across European countries in the first pandemic year. | [figure_2_S7_S8](./notebooks/figure_2_S7_S8.ipynb) |
| 3      | Out-household COVID-19 spread across European countries. | [charts](./notebooks/charts.ipynb) |
| 4      | Effective household size η∗ and the out-household rep. number R_out influence the correlation between COVID-19 prevalence α and the Human Development Index (HDI). | [charts](./notebooks/charts.ipynb) |
| S1     | Country infection fatality rate (CIFR) estimation for different countries. | [charts](./notebooks/charts.ipynb) |
| S2     | Example estimation of total COVID-19 deaths for Bulgaria and Spain. | [charts](./notebooks/charts.ipynb) |
| S3     | The officially reported number of COVID-19 deaths, surplus deaths, and γ-Extended deaths. | [charts](./notebooks/charts.ipynb) |
| S4     | Prevalence estimation for different countries. | [charts](./notebooks/charts.ipynb) |
| S5     | Number of emergency procedures due to all causes except COVID-19 in Poland. | [charts](./notebooks/charts.ipynb) |
| S6     | Robustness of our results before variations in assumed parameters. | [figure_S6](./notebooks/figure_S6.ipynb) |
| S7     | Relation between prevalence and effective household sizes. | [figure_2_S7_S8](./notebooks/figure_2_S7_S8.ipynb) |
| S8     | Critical out-household reproduction number | [figure_2_S7_S8](./notebooks/figure_2_S7_S8.ipynb) |



### Reproduction of the data processing

Download the required death [data](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/DEMO_R_MWK2_05/?format=SDMX-CSV&lang=en&label=both) and save it to ./data/Deaths.csv

Run the notebook [main](./notebooks/main.ipynb) for sampling of the CIFR, it will write the prevelance samples to ./data/prevalence_vectors.

Next, run the script ./code/process_data.py, which will read the sampled prevalence estimations from ./data/prevalence_vectors, and write the calculated out-household reproduction number and predicted prevalence given mean R_out to according files in ./data/processed.

Run the plotting notebooks listed above to reproduce the figures.

