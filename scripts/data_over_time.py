""" The purpose of this file is to aggregate data from the bitcoin network
    over time
"""
import sys

import networkx as nx 
import graphgen
import graphtools
import tags_over_time
from networkx.algorithms import *

_HMS = 1000000
slices = graphgen.generate_time_slices(slice_time=5, num_intervals=50, num_in_slice=10)
i = 0
deg_connectivity = []
dates = []
avg_clust = []
lccs = []
largest_scc = []
for start, end in slices:
  g = graphgen.get_graph_slice(start * _HMS, end * _HMS)
  stamp = str(start) + '_' + str(end)
  tags_over_time.user_transaction_frequency(g, stamp)
  tags_over_time.user_transaction_amount(g, stamp)
  tags_over_time.user_buy_frequency(g, stamp)
  tags_over_time.user_sell_frequency(g, stamp)
  
  d = assortativity.average_degree_connectivity(g)
  tags_over_time.save_node_map(d, stamp)
  l.append(assortativity.average_degree_connectivity(g))

  avg_clust.append(clustering.average_clustering(g))
  lccs.append(len(graphtools.get_lcc_from_graph(g)))
  largest_scc.append(len(graphtools.get_sccs_from_graph(g)[0]))
  dates.append(start) # hack for now to save time...
  
  print 'finished %s tag over time' % i
  i += 1


# plot single values over time
# Gini coefficient (way to get single number from distribution)






