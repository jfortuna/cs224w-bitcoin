import networkx as nx
import numpy as np

from numpy.random import *


def consumer_vendor_graph(c, v, purchase_rate=3, pop_exp=1, menu_variance=1, duration=None):
    """
    Generate a graph with vendors and consumers, where vendors sell a
    product, consumers buy the product, and also interact with one
    another.

    Some assumptions:
    Popularity of vendors is distributed as a power law.
    Each vendor's menu is distributed normally with constant variance.
    Each vendor's menu's mean is sampled from a zero-mean normal distribution
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
    vend_pop = dict([(i, power(pop_exp)) for i in range(v)])
    vend_menu = dict([(i, normal(scale=np.sqrt(menu_variance))) for i in range(v)])
    
    # Map from consumer to the number of purchases they make
    cons = dict([(i, _transaction_times(purchase_rate, duration)) for i in range(v, c + v)])

    # Add vendor -> cons links
    for con in cons:
        # Loop over each of the transaction times
        for timestamp in cons[con]:
            # Sample a vendor
            trans_vendor = _sample_dist(vend_pop)
            trans_value = normal(loc=vend_menu[trans_vendor], scale=menu_variance)
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
