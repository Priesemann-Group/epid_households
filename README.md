Household size can explain 40% of the variance in cumulative COVID-19 incidence across Europe
arxiv.org/abs/2602.15447


The main analysis is done by running the short script ./code/process_data.py,
which executes the relevant code implemented in ./code/households.py.
This will read the sampled prevalence estimations for different gamma from ./data/prevalence_vectors,
and write the calculated out-household reproduction number and predicted prevalence given mean R_out to according files in ./data/processed.
The ./figure/* are plotted by jupyter notebooks found in ./notebooks.

