""" The purpose of this file is to aggregate data from the bitcoin network
    over time
"""
import sys
import utils
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
  if len(g) == 0:
    continue
 # stamp = str(start) + '_' + str(end)
  #tags_over_time.user_transaction_frequency(g, stamp)
 # tags_over_time.user_transaction_amount(g, stamp)
 # tags_over_time.user_buy_frequency(g, stamp)
 # tags_over_time.user_sell_frequency(g, stamp)
  
 # d = assortativity.average_degree_connectivity(g)
 # utils.save_node_map(d, stamp)
  deg_connectivity.append(assortativity.average_degree_connectivity(g))
  undir_g = nx.Graph(g.copy())
  avg_clust.append(nx.average_clustering(undir_g))
  lccs.append(len(graphtools.get_lcc_from_graph(g)))
  largest_scc.append(len(graphtools.get_sccs_from_graph(g)[0]))
  dates.append(start) # hack for now to save time...
  
  print 'finished %s tag over time' % i
  i += 1

utils.save_lists(dates, deg_connectivity, stamp='deg_conn')
utils.save_lists(dates, avg_clust, stamp='avg_clust')
utils.save_lists(dates, lccs, stamp='lccs')
utils.save_lists(dates, largest_scc, stamp='largest_scc')
# plot single values over time
# Gini coefficient (way to get single number from distribution)






