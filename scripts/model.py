import networkx as nx
import numpy as np
import scipy.stats as sts
import random

from numpy.random import *
from graphgen import *
from graphtools import *
from math import log

def cv_from_btc(start, end):
    """
    Give it a start and an end time, and it randomly generates a cv-graph
    to match that time slice
    """
    g = get_graph_slice(start, end)
    if len(g) == 0:
        return g
    v = len(g) / 100
    c = len(g) - v
    s2d = lambda t: string_to_datetime(str(t))
    duration = 604800
    if 'total_seconds' in dir(s2d(end) - s2d(start)):
        duration = (s2d(end) - s2d(start)).total_seconds()
    rate = float(len(g.edges())) / (c * duration)
    powerlaw = 1 + len(g) / sum(map(lambda x: log(x), g.degree().values()))
    vals = map(lambda e: e[2]['value'] / 2, g.edges(data=True))
    std = np.std(vals + map(lambda x: -1.0 * x, vals))
    # default behavior, ignore computed duration
    return consumer_vendor_graph(c, v, purchase_rate=1.0/rate, pop_exp=powerlaw, menu_variance=std**2, duration=duration)


def sample_powerlaw(alpha):
    u = random.random()
    return u**(1.0/(1-alpha))    

def fit_powerlaw(vals):
    max_val = max(vals)
    freqs = np.zeros(max_val)

    for i in vals:
        freqs[i-1] += 1

    xs = np.array([log(x+1) for x in filter(lambda x: freqs[x] != 0, range(max_vals))])
    ys = np.array([log(float(freqs[x]) / len(vals)) for x in filter(lambda x: freqs[x] != 0, range(max_vals))])
    linreg = sts.linregress(xs[10:100],ys[10:100])        
    return -linreg[0]
    

def consumer_vendor_graph(c, v, purchase_rate=3, pop_exp=1, menu_variance=1, duration=None):
    """
    Generate a graph with vendors and consumers, where vendors sell a
    product, consumers buy the product, and also interact with one
    another, maybe.

    Some assumptions:
    Popularity of vendors is distributed as a power law.
    Each transaction is sampled from a zero-mean gaussian.
    Purchases are modeled as Poisson processes.

    Parameters:
    c             - number of consumers
    v             - number of vendors
    pop_exp       - exponent of power law for vendor popularity
    purchase_rate - lambda/rate for consumer purchases
    menu_variance - the variance of the distribution of menu means
    duration      - length of time the graph should represent
                    default is None, which is replaced by one week
    """
    G = nx.MultiDiGraph()

    # Default duration is one week, i.e. 604800 seconds
    if duration is None:
        duration = 604800

    # Map from vendor to popularity
    vend_pop = dict([(i, sample_powerlaw(pop_exp)) for i in range(v)])
    
    # Map from consumer to the number of purchases they make
    cons = dict([(i, _transaction_times(purchase_rate, duration)) for i in range(v, c + v)])

    # Add vendor -> cons links
    for con in cons:
        # Loop over each of the transaction times
        for timestamp in cons[con]:
            # Sample a vendor
            trans_vendor = _sample_dist(vend_pop)
            trans_value = normal(scale=menu_variance)
            if trans_value < 0:
                G.add_edge(trans_vendor, con, value=(-1 * trans_value), time=timestamp)
            else:
                G.add_edge(con, trans_vendor, value=trans_value, time=timestamp)

    # TODO: Add links between consumers
    #       Totally a maybe todo, might be fine without
    
    return G



def _transaction_times(rate, duration):
    """
    Get a list of times at which transactions occur for a user
    with given transaction rate who is making transactions during a given duration
    """
    times = []
    while True:
        sample = exponential(rate)
        last = 0 if len(times) == 0 else times[-1]
        if sample + last > duration:
            break
        times.append(sample + last)
    return times
    

def _sample_dist(d):
    """
    Takes a dict d with keys (items) and vals (weights) and samples from
    the items by their relative weights.
    """
    r = uniform(0, sum(d.itervalues()))
    s = 0.0
    key = -1
    for key, weight in d.iteritems():
        s += weight
        if r < s: 
            return key
    return key
