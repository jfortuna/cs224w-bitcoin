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

def bucketed_sccs(g, stamp=''):
    sccs = graphtools.get_sccs_from_graph(g)
    buckets = _count_size_of_property(sccs)


def avg_out_degree_over_time():
    avg_out_degrees = {}
    graph = nx.MultiDiGraph()
    for end_day in graphgen._days:
        start = int(str(end_day) + "000000")
        end = int(str(end_day) + "235959")
        graph = graphgen.add_slice_to_graph(graph, start, end)
        avg_out_deg = graphtools.get_avg_out_degree_from_graph(graph)
        avg_out_degrees[end_day] = avg_out_deg
        print end_day, avg_out_deg
    utils.save_node_map(avg_out_degrees, ("avg_out_degrees"))


def nodes_vs_edges_over_time():
    num_nodes = []
    num_edges = []
    graph = nx.MultiDiGraph()
    for end_day in graphgen._days:
        start = int(str(end_day) + "000000")
        end = int(str(end_day) + "235959")
        graph = graphgen.add_slice_to_graph(graph, start, end)
        nodes, edges = graphtools.get_num_nodes_edges_from_graph(graph)
        num_nodes.append(nodes)
        num_edges.append(edges)
        print nodes, edges
    utils.save_lists(num_nodes, num_edges, ("nodes_vs_edges"))


def frac_nodes_in_gcc_over_time():
    frac_nodes_in_gcc = {}
    graph = nx.MultiDiGraph()
    for end_day in graphgen._days:
        start = int(str(end_day) + "000000")
        end = int(str(end_day) + "235959")
        graph = graphgen.add_slice_to_graph(graph, start, end)
        frac_nodes = graphtools.get_frac_nodes_in_gcc_from_graph(graph)
        frac_nodes_in_gcc[end_day] = frac_nodes
        print end_day, frac_nodes
    utils.save_node_map(frac_nodes_in_gcc, ("frac_nodes_in_gcc"))


def effective_diameter_over_time():
    effective_diameters = {}
    graph = nx.MultiDiGraph()
    for end_day in graphgen._days:
        start = int(str(end_day) + "000000")
        end = int(str(end_day) + "235959")
        graph = graphgen.add_slice_to_graph(graph, start, end)
        effective_diam = graphtools.effective_diameter(graph)
        effective_diameters[end_day] = effective_diam
        print end_day, effective_diam
    utils.save_node_map(effective_diameters, ("effective_diameters"))


def main(args):
    if len(args) == 1:
        arg = args[0]
        if arg == '1':
            avg_out_degree_over_time()
        elif arg == '2':
            nodes_vs_edges_over_time()
        elif arg == '3':
            frac_nodes_in_gcc_over_time()
        elif arg == '4':
            effective_diameter_over_time()
        else:
            print "Usage: 1, 2, 3, 4"
    else:
        print "Usage: 1, 2, 3, 4"


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
