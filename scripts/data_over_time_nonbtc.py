""" The purpose of this file is to aggregate data from the bitcoin network
    over time
"""
import sys
import utils
import networkx as nx 
import graphgen
import graphtools
import tags_over_time
import forest_fire
from networkx.algorithms import *
'''
_HMS = 1000000
slices = graphgen.generate_weighted_time_slices()
i = 0
dates = []
avg_clust = []
lccs = []
largest_scc = []
dates = []
avg_clust_p = []
lccs_p = []

for start, end in slices:
  g = graphgen.get_graph_slice(start * _HMS, end * _HMS)
  if len(g) == 0:
    continue
  rg = nx.gnm_random_graph(g.number_of_nodes(), g.number_of_edges(), directed=True)
  pfg = nx.barabasi_albert_graph(g.number_of_nodes(), g.number_of_edges()/g.number_of_nodes())
  stamp = str(start) + '_' + str(end)
  
  tags_over_time.user_transaction_frequency(pfg, 'pfg_' + stamp)
 # tags_over_time.user_transaction_amount(pfg, 'pfg_' + stamp)
  #tags_over_time.user_buy_frequency(pfg, 'pfg_' + stamp)
  #tags_over_time.user_sell_frequency(pfg, 'pfg_' + stamp)

  tags_over_time.user_transaction_frequency(rg, 'rg_' + stamp)
  #tags_over_time.user_transaction_amount(rg, 'rg_' + stamp)
  tags_over_time.user_buy_frequency(rg, 'rg_' + stamp)
  tags_over_time.user_sell_frequency(rg, 'rg_' + stamp)
  
  # d = assortativity.average_degree_connectivity(g)
  # utils.save_node_map(d, 'gnp_avg_deg_conn_' + stamp)
  # deg_connectivity.append(assortativity.average_degree_connectivity(g))
  undir_g_r = nx.Graph(rg.copy())
  avg_clust.append(nx.average_clustering(undir_g_r))
  lccs.append(len(graphtools.get_lcc_from_graph(rg)))
  largest_scc.append(len(graphtools.get_sccs_from_graph(rg)[0]))
  
  dates.append(start) # hack for now to save time...

  undir_g_p = nx.Graph(pfg.copy())
  avg_clust_p.append(nx.average_clustering(undir_g_p))
  lccs_p.append(len(graphtools.get_lcc_from_graph(pfg)))
  
  print 'finished %s tag over time' % i
  i += 1

# utils.save_lists(dates, deg_connectivity, stamp='gnp_deg_conn')
utils.save_lists(dates, avg_clust, stamp='gnp_avg_clust')
utils.save_lists(dates, lccs, stamp='gnp_lccs')
utils.save_lists(dates, largest_scc, stamp='gnp_largest_scc')

utils.save_lists(dates, avg_clust_p, stamp='pfg_avg_clust')
utils.save_lists(dates, lccs_p, stamp='pfg_lccs')
# plot single values over time
# Gini coefficient (way to get single number from distribution)
'''



_HMS = graphgen._HMS
slices = graphgen.generate_weighted_time_slices()
i = 0
dates = []
avg_clust = []
lccs = []
largest_scc = []

p = 0.37
p_b = 0.32
r = p / p_b

for start, end in slices:
    g = graphgen.get_graph_slice(start * _HMS, end * _HMS)
    if len(g) == 0:
        continue
    ff = forest_fire.gen_forest_fire(g.number_of_nodes(), p, r)
    stamp = str(start) + '_' + str(end)
    
    tags_over_time.user_transaction_frequency(ff, 'ff_' + stamp)
    tags_over_time.user_buy_frequency(ff, 'ff_' + stamp)
    tags_over_time.user_sell_frequency(ff, 'ff_' + stamp)
  
    undir_ff = nx.Graph(ff.copy())
    avg_clust.append(nx.average_clustering(undir_ff))
    lccs.append(len(graphtools.get_lcc_from_graph(ff)))
    largest_scc.append(len(graphtools.get_sccs_from_graph(ff)[0]))
    
    dates.append(start) # hack for now to save time...
    
    print 'finished %s tag over time' % i
    i += 1

utils.save_lists(dates, avg_clust, stamp='ff_avg_clust')
utils.save_lists(dates, lccs, stamp='ff_lccs')
utils.save_lists(dates, largest_scc, stamp='ff_largest_scc')

