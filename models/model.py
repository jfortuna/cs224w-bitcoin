import networkx as nx
import numpy as np
import random


def consumer_producer_graph(c, p, purchase_rate=3, pop_var=1):
    """
    Generate a graph with producers and consumers, where producers sell a
    product, consumers buy the product, and also interact with one
    another.

    Popularity of producers is distributed normally.
    Each producer's menu is distributed normally.
    Purchases are modeled as Poisson processes.
    """
    # number of consumers
    # number of producers
    # purchase rate
    # 

    G = nx.MultiDiGraph()

    # Map from producer to menu and popularity
    prod = {i: abs(np.random.normal(scale=pop_var)) for i in range(p)}
    
    # Map from consumer to the number of purchases they make
    cons = {i: np.random.poisson(lam=purchase_rate) for i in range(p, c + p)}

    # Add prod -> cons links
    for con in cons:
        for _ in range(cons[con]):
            # TODO: add weights by menu price
            G.add_edge(con, _sampleDist(prod))

    # TODO: Add links between consumers
    
    return G
    

def _sampleDist(d):
    r = random.uniform(0, sum(d.itervalues()))
    s = 0.0
    key = -1
    for key, weight in d.iteritems():
        s += weight
        if r < s: 
            return key
    return key

    
