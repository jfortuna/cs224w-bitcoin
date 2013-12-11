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

def _node_and_edges(start, end):
    g = graphgen.get_graph_slice(start * 1000000, end * 1000000)
    if len(g) == 0:
        return 0, 0
    return g.number_of_nodes(), g.number_of_edges()


def avg_out_degree_over_time():
    slices = graphgen.generate_weighted_time_slices()

    avg_out_degrees_r = {}
    avg_out_dgree_p = {}
    for start, end in slices:
        n, m = _node_and_edges(start, end)
        if n == 0:
            continue
        rg = nx.gnm_random_graph(n, m, directed=True)
        pfg = nx.barabasi_albert_graph(n, m/n)
  
        avg_out_deg = graphtools.get_avg_out_degree_from_graph(rg)
        avg_out_degrees_r[start] = avg_out_deg
        avg_out_deg = graphtools.get_avg_out_degree_from_graph(pfg)
        avg_out_degrees_p[start] = avg_out_deg
        
    utils.save_node_map(avg_out_degrees_r, ("avg_out_degrees_r"))
    utils.save_node_map(avg_out_degrees_p, ("avg_out_degrees_p"))


def nodes_vs_edges_over_time():
    num_nodes = []
    num_edges = []
    slices = graphgen.generate_weighted_time_slices()

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
    slices = graphgen.generate_weighted_time_slices()

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
    slices = graphgen.generate_weighted_time_slices()

    graph = nx.MultiDiGraph()
    for end_day in graphgen._days:
        start = int(str(end_day) + "000000")
        end = int(str(end_day) + "235959")
        graph = graphgen.add_slice_to_graph(graph, start, end)
        effective_diam = graphtools.effective_diameter(graph)
        effective_diameters[end_day] = effective_diam
        print end_day, effective_diam
    utils.save_node_map(effective_diameters, ("effective_diameters"))


def all_computations():
    slices = graphgen.generate_weighted_time_slices()

    avg_out_degrees_r = {}
    # effective_diameters_p = {}
    # effective_diameters_r = {}
    frac_nodes_in_gcc_p = {}
    frac_nodes_in_gcc_r = {}

    i = 0
    for start, end in slices:
        print 'slice %s of %s' % (i, len(slices))
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
    # if len(args) == 1:
    #     arg = args[0]
    #     if arg == '1':
    #         avg_out_degree_over_time()
    #     elif arg == '2':
    #         nodes_vs_edges_over_time()
    #     elif arg == '3':
    #         frac_nodes_in_gcc_over_time()
    #     elif arg == '4':
    #         effective_diameter_over_time()
    #     else:
    #         print "Usage: 1, 2, 3, 4"
    # else:
    #     all_computations()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
