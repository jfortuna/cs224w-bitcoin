""" Rough Idea for this script is to use Julie's functions that
    return dicts or lists of lists, and make them into meaningful
    bucket systems. Perhaps number of scc's at that point in time
    for instance?
"""

import sys
import graphtools
import graphgen
import utils
import networkx as nx
from model import *


def all_computations():
    slices = graphgen.generate_weighted_time_slices()
    avg_out_degrees = {}
    frac_nodes_in_gcc = {}
    num_nodes = []
    num_edges = []
    for i in range(len(slices)):
        print i, " slices out of ", len(slices)
        start, end = slices[i]
        g = cv_from_btc(start, end)
        if len(g) == 0:
            continue
        num_nodes.append(g.number_of_nodes())
        num_edges.append(g.number_of_edges())
        avg_out_deg = graphtools.get_avg_out_degree_from_graph(g)
        avg_out_degrees[start] = avg_out_deg

        frac_nodes = graphtools.get_frac_nodes_in_gcc_from_graph(g)
        frac_nodes_in_gcc[start] = frac_nodes

    utils.save_node_map(avg_out_degrees, ("avg_out_degrees_model"))

    utils.save_node_map(frac_nodes_in_gcc, ("frac_nodes_in_gcc_model"))
    utils.save_lists(num_nodes, num_edges, ("nodes_vs_edges_model"))

def main(args):
    all_computations()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
