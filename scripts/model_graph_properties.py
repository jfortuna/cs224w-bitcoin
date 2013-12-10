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

def _node_and_edges(start, end):
    g = graphgen.get_graph_slice(start * _HMS, end * _HMS)
    if len(g) == 0:
        return 0, 0
    return g.number_of_nodes(), g.number_of_edges()


def all_computations():
    slices = graphgen.generate_weighted_time_slices()

    avg_out_degrees_r = {}
    # effective_diameters_p = {}
    # effective_diameters_r = {}
    frac_nodes_in_gcc_p = {}
    frac_nodes_in_gcc_r = {}


    for start, end in slices:
        n, m = _node_and_edges(start, end)
        if n == 0:
            continue
        rg = nx.gnm_random_graph(n, m, directed=True)
        pfg = nx.barabasi_albert_graph(n, m/n)
  
        avg_out_deg = graphtools.get_avg_out_degree_from_graph(rg)
        avg_out_degrees_r[start] = avg_out_deg
        # effective_diam = graphtools.effective_diameter(rg)
        # effective_diameters_r[start] = effective_diam
        # effective_diam = graphtools.effective_diameter(pfg)
        # effective_diameters_p[start] = effective_diam

        frac_nodes = graphtools.get_frac_nodes_in_gcc_from_graph(rg)
        frac_nodes_in_gcc_r[start] = frac_nodes
        frac_nodes = graphtools.get_frac_nodes_in_gcc_from_graph(pfg)
        frac_nodes_in_gcc_p[start] = frac_nodes

        
    utils.save_node_map(avg_out_degrees_r, ("avg_out_degrees_r"))
    # utils.save_node_map(effective_diameters_r, ("effective_diameters_r"))
    # utils.save_node_map(effective_diameters_p, ("effective_diameters_p"))

    utils.save_node_map(frac_nodes_in_gcc_r, ("frac_nodes_in_gcc_r"))
    utils.save_node_map(frac_nodes_in_gcc_p, ("frac_nodes_in_gcc_p"))

def main(args):
    all_computations()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
