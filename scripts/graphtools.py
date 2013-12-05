import graphgen
import networkx as nx
from datetime import datetime

def get_wccs_from_graph(graph):
    return nx.weakly_connected_components(graph)

def get_wccs_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    return nx.weakly_connected_components(g_slice)

def get_lcc_from_graph(graph):
    return get_wccs_from_graph(graph)[0]

def get_lcc_from_dates(start, end):
    return get_wccs_from_dates(start, end)[0]

def get_sccs_from_graph(graph):
    return nx.strongly_connected_components(graph)

def get_sccs_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    return nx.strongly_connected_components(graph)

def get_in_degrees_from_graph(graph):
    return graph.in_degree()

def get_in_degrees_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    return g_slice.in_degree()

def get_node_max_in_degree(graph):
    in_degrees = get_in_degrees_from_graph(graph)
    return max(in_degrees, key=in_degrees.get)

def get_out_degrees_from_graph(graph):
    return graph.out_degree()

def get_out_degrees_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    return g_slice.out_degree()

def get_k_core_from_graph(graph):
    return nx.k_core(graph)

def string_to_datetime(string):
    if len(string) == 14:
        return datetime.strptime(string, "%Y%m%d%H%M%S")
    else:
        return datetime.strptime(string, "%Y%m%d")
