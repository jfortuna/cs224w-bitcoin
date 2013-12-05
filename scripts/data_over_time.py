""" The purpose of this file is to aggregate data from the bitcoin network
    over time
"""
import sys

import networkx as nx 
import graphgen
import tags_over_time

_HMS = 1000000


slices = graph_gen_utils.generate_time_slices(num_intervals=10, num_in_slice=1)
i = 0
for start, end in slices:
  g = graphgen.get_graph_slice(start * _HMS, end * _HMS)
  tags_over_time.user_transaction_frequency(g, str(start) + '_' + str(end))
  print 'finished %s tag over time' % i
  i += 1
