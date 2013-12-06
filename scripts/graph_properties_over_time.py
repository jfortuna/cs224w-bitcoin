""" Rough Idea for this script is to use Julie's functions that
    return dicts or lists of lists, and make them into meaningful
    bucket systems. Perhaps number of scc's at that point in time
    for instance?
"""

import graphtools
import networkx as nx 

def bucketed_sccs(g, stamp=''):
  sccs = graphtools.get_sccs_from_graph(g)
  buckets = _count_size_of_property(sccs)


