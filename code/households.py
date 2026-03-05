import numpy as np
import pandas as pd
from scipy.optimize import fsolve
from scipy.special import binom
from scipy.stats import pearsonr
import time


# ISO codes:
isos = pd.read_csv('../data/isos.csv', sep=',', header=0)
# Size Distributions from Eurostat: 
eurostat = pd.read_csv('../data/2021_SizeDist.csv', sep=',',header=0)
# European population size from Eurostat:
population = pd.read_csv('../data/europe_populationsize.csv', sep=',', header=0)


def get_iso2(name):
    if name == 'United Kingdom':
        return 'UK'
    else: 
        return list(isos[isos['name'] == name]['alpha-2'])[0]

def get_distribution(iso):
    if iso=='AL': return get_distribution_albania()
    country = eurostat[eurostat['geo'] == iso]
    country_latest = country[country['TIME_PERIOD'] == 2019]
    if len(list(country_latest['TIME_PERIOD'])) == 0:
        country_latest = country[country['TIME_PERIOD'] == 2018]
    distribution = np.array(list(country_latest['OBS_VALUE']))/100
    return distribution

# Albania's and North Macedonia's household distributions are in some other files 
def get_distribution_albania():
    datafile = pd.read_csv('../data/ilc_lvph03_1_Data.csv',sep=',',header=0)
    albania = datafile[datafile['GEO'] == 'Albania']
    dist = np.asarray(albania['Value'],dtype=float)/100
    return dist

def get_distribution_northmacedonia():
    datafile = pd.read_csv('../data/ilc_lvph03_1_Data.csv',sep=',',header=0)
    macedonia = datafile[datafile['GEO'] == 'North Macedonia']
    dist = np.asarray(macedonia['Value'],dtype=float)/100
    return dist

def get_population(iso):
    return int(population[ (population['geo']==iso) & (population['TIME_PERIOD']==2019)]['OBS_VALUE'])

def get_polulation_array(countries):
    array = np.zeros(len(countries))
    for i,country in enumerate(countries):
        array[i] = get_population(get_iso2(country))
    return array

def get_european_distribution(countries):
    dist = np.zeros(6)
    for country in countries:
        iso = get_iso2(country)
        tmp = (get_distribution(iso)*[1,2,3,4,5,6])
        tmp /= tmp.sum()
        tmp *= get_population(iso)
        dist += tmp
    dist /= [1,2,3,4,5,6]
    dist /= dist.sum()
    return dist


# With eta, alpha and a_h as input (for calculating c(alpha))
def f(p, *args):
    eta=args[0]
    alpha=args[1]
    mus = args[2]
    
    summe = 0
    E = 0
    for i in range(len(eta)):
        summe = summe + eta[i]*calc_mu(i+1, p, mus)
        E = E + eta[i]*(i+1)
    return (summe - E*alpha)
  
# with eta, c and a_h as input (for calculating alpha(c)) 
def g(alpha, *args):
    eta = args[0]
    c = args[1]
    mus = args[2]
    
    summe = 0
    E = 0
    for i in range(len(eta)):
        summe = summe + eta[i]*calc_mu_2(i+1, alpha, c, mus)
        E = E + eta[i]*(i+1)
    return (summe - E*alpha)



# For the "forward calculation" of c(alpha)    
def calc_mu(k,p,mus):
    if k == 1:
        return p
    else:
        mu = 0
        for l in np.linspace(1,k,k):
            l = int(l)
            mu+= binom(k,l)*p**l*(1-p)**(k-l)*get_mukl(k,l,mus)
        return mu 
    
    
# For the "backward calculation" of alpha(average european c)
def calc_mu_2(k,alpha,c,mus):
    if k == 1:
        return calc_p(alpha, c)
    else:
        mu = 0
        for l in np.linspace(1,k,k):
            l = int(l)
            mu+= binom(k,l)*calc_p(alpha, c)**l*(1-calc_p(alpha, c))**(k-l)*get_mukl(k,l,mus)
        return mu 



# Forward calculation of c(alpha) 
# First p \in [0,1] is calculated in case any error occurs
def pc(hh_dist, alpha, mus):
    p = fsolve(f, 0.5, args =(hh_dist, alpha, mus))
    if p<=0 or p>=1:
        print('Error: p outside of bounds')
    c = calc_c(alpha, p)
    return [p,c]

def calc_c(alpha, p):
    return -np.log(1-p)/alpha

def calc_p(alpha, c):
    return 1-np.exp(-alpha*c)

def get_mukl(k,l,mus):
    return np.array(mus[k-2][l-1])


# Backward calculation of alpha(average european c) 
def alpha(hh_dist, c, alph, mus):
    alpha = fsolve(g, alph, args=(hh_dist, c, mus))
    return alpha

def momentratio(dist):
    m1=0
    m2=0
    for i in range(len(dist)):
        m1 = m1+dist[i]*(i+1)
        m2 = m2+dist[i]*(i+1)**2
    return m2/m1

# Calculation of mus, formulars from Tyll

def mu(k,l,p):
    s = 0
    for m in range(1,k+1):
        s += m*P_hat(k,l,m,p)    
    return s

def P_hat(k,l,m,p):
    if l==1: return C(k,m,p)
    if l>k: return 0
    s = 0
    for x in range(l-1,m):
        s += ( P_hat(k,l-1,x,p) * P_hat(k-x,1,m-x,p) * ( (k-x) / (k-(l-1)) ) )
    s += P_hat(k,l-1,m,p)*(1-(k-m)/(k-(l-1)))
    return s

def C(n,k,p):
    return binom(n-1,k-1)*P(k,p)*(1-p)**(k*(n-k))

def P(n,p):
    if n==1: return 1
    s = 0
    for k in range(1,n):
        s += binom(n-1,k-1) * P(k,p) * (1-p)**(k*(n-k))
    return 1-s

def a_C(n,p):
    s = 0
    for k in range(1,n+1):
        s += C(n,k,p)*(k-1)/(n-1)
    return s

def get_fun(n, a_h):
    return lambda p:a_C(n,p)-a_h

def calc_mus(a_h):
    ns = np.array([2,3,4,5,6])
    p_t = np.zeros(len(ns))

    for i,n in enumerate(ns):
        fun = get_fun(n, a_h)
        p_t[i] = fsolve(fun, a_h)[0]

    mus = np.zeros((5,6))
    for k in [2,3,4,5,6]:
        for l in [1,2,3,4,5,6]:
            mus[k-2,l-1] = mu(k,l,p_t[k-2])
    return mus


# higher level stuff

def calc_explained_variance(real, theo):
    residuals = np.mean((real-theo)**2)
    return 1-(residuals/np.var(real))

def calc_pearson(sample):
    prev = sample
    mratio = sample.index.map(get_iso2).map(get_distribution).map(momentratio)
    return pearsonr(prev, mratio)[0]

def read_data(path):
    data = pd.read_csv(path, index_col=0) /100
    data.drop(columns=['Liechtenstein'], inplace=True)
    return data

def filter_strikt(data):
    dataf = data.copy()
    for country in dataf.columns:
        dataf[country][data[country]<np.percentile(data[country],2.5)] = np.nan
        dataf[country][data[country]>np.percentile(data[country],97.5)] = np.nan
    dataf.dropna(inplace=True)
    dataf.reset_index(drop=True, inplace=True)
    print(data.shape[0] - dataf.shape[0], "datapoints dropped via 5% filter")
    return data

def filter_soft(data):
    dataf2 = data.copy()
    dataf2[data>1] = np.nan
    dataf2.dropna(inplace=True)
    dataf2.reset_index(drop=True, inplace=True)
    print(data.shape[0] - dataf2.shape[0], "datapoints dropped bc prevalence > 1")
    return dataf2

def calc_data_c(data, mus):
    data_c = pd.DataFrame(index=data.index, columns=data.columns)
    for country in data_c.columns:
        start_time = time.time()
        dist = get_distribution(get_iso2(country))
        data_c.loc[:,country] = data[country].map(lambda x: pc(dist, x, mus)[1].item())
        print(country, time.time()-start_time)
    return data_c

def calc_european_means(data, data_c, mus):
    european_means = pd.DataFrame(index=data_c.index, columns=['basic_mean', 'weighted_mean', 'europe_as_country'])

    european_means.loc[:,'basic_mean'] = data_c.mean(axis=1)

    weights = get_polulation_array(data_c.columns)
    weights /= weights.sum()
    european_means.loc[:,'weighted_mean'] = (data_c*weights).sum(axis=1)

    eu_incidence = (data*weights).sum(axis=1)
    eu_dist = get_european_distribution(data_c.columns)
    european_means.loc[:,'europe_as_country'] = eu_incidence.map(lambda x: pc(eu_dist, x, mus)[1].item())

    return european_means

# calc a (for fixed european mean)
def calc_data_a(data_c, means, mus):
    data_alpha_predict = pd.DataFrame(index=data_c.index, columns=data_c.columns)
    for country in data_alpha_predict.columns:
        start_time = time.time()
        dist = get_distribution(get_iso2(country))
        mratio = momentratio(dist)
#    guess = mratio * 0.4/3 - 1.8 + 2*0.8
#    guess = 0.5
        guess = 1.0
        data_alpha_predict.loc[:,country] = means.map(lambda x: alpha(dist, x, guess, mus).item())
        print(country, time.time()-start_time)
    return data_alpha_predict

def calc_data_a_hhdist(data_c, mus):
    data_alpha_predict_hhdist = pd.DataFrame(index=data_c.index, columns=data_c.columns)
    europe = eurostat[eurostat['geo'] == 'EU']
    europe = europe[europe['TIME_PERIOD'] == 2019]
    dist_europe = np.array(list(europe['OBS_VALUE']))/100
    for country in data_alpha_predict_hhdist.columns:
        start_time = time.time()
        guess = 0.5
        data_alpha_predict_hhdist.loc[:,country] = data_c.loc[:,country].map(lambda x: alpha(dist_europe, x, guess, mus).item())
        print(country, time.time()-start_time)
    return data_alpha_predict_hhdist

def run_all(gamma, a_h, mean='europe_as_country', hhdist=False):
    data = filter_soft(read_data("../results/prevalence_vectors/Prevalence2021W22(gamma={}).csv".format(gamma)))
    mus = calc_mus(a_h)
    data_c = calc_data_c(data, mus)
    european_means = calc_european_means(data, data_c, mus)
    means = european_means[mean]
    data_a = calc_data_a(data_c, means, mus)
    data.to_csv('../results/processed/(gamma={},ah={},{})_data.csv'.format(gamma,a_h,mean))
    data_c.to_csv('../results/processed/(gamma={},ah={},{})_data_c.csv'.format(gamma,a_h,mean))
    data_a.to_csv('../results/processed/(gamma={},ah={},{})_data_a.csv'.format(gamma,a_h,mean))
    if hhdist==True:
        data_a_hhdist = calc_data_a_hhdist(data_c, mus)
        data_a_hhdist.to_csv('../results/processed/(gamma={},ah={},{})_data_a_hhdist.csv'.format(gamma,a_h,mean))
    return 1

