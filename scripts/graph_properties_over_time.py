""" Rough Idea for this script is to use Julie's functions that
    return dicts or lists of lists, and make them into meaningful
    bucket systems. Perhaps number of scc's at that point in time
    for instance?
"""

import graphtools
import graphgen
import utils
import networkx as nx 

def bucketed_sccs(g, stamp=''):
    sccs = graphtools.get_sccs_from_graph(g)
    buckets = _count_size_of_property(sccs)


def avg_out_degree_over_time():
    avg_out_degrees = {}
    start = int(str(graphgen._days[0]) + "000000")
    for end_day in graphgen._days:
        end = int(str(end_day) + "235959")
        avg_out_deg = graphtools.get_avg_out_degree_from_dates(start, end)
        avg_out_degrees[end] = avg_out_deg
        print end, avg_out_deg
    utils.save_node_map(avg_out_degrees, ("avg_out_degrees"))


def nodes_vs_edges_over_time():
    num_nodes = []
    num_edges = []
    start = int(str(graphgen._days[0]) + "000000")
    for end_day in graphgen._days:
        end = int(str(end_day) + "235959")
        nodes, edges = graphtools.get_num_nodes_edges_from_dates(start, end)
        num_nodes.append(nodes)
        num_edges.append(edges)
        print nodes, edges
    utils.save_lists(num_nodes, num_edges, ("nodes_vs_edges"))


def frac_nodes_in_gcc_over_time():
    frac_nodes_in_gcc = {}
    start = int(str(graphgen._days[0]) + "000000")
    for end_day in graphgen._days:
        end = int(str(end_day) + "235959")
        frac_nodes = graphtools.get_frac_nodes_in_gcc_from_dates(start, end)
        frac_nodes_in_gcc[end] = frac_nodes
        print end, frac_nodes
    utils.save_node_map(frac_nodes_in_gcc, ("frac_nodes_in_gcc"))


def effective_diameter_over_time():
    effective_diameters = {}
    start = int(str(graphgen._days[0]) + "000000")
    for end_day in graphgen._days:
        end = int(str(end_day) + "235959")
        effective_diam = graphtools.get_effective_diameter_from_dates(start, end)
        effective_diameters[end] = effective_diam
        print end, effective_diam
    utils.save_node_map(effective_diameters, ("effective_diameters"))


#avg_out_degree_over_time()
#nodes_vs_edges_over_time()
#frac_nodes_in_gcc_over_time()
#effective_diameter_over_time()
