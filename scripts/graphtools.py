import graphgen
import networkx as nx

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
    pass

def get_in_degrees_from_dates(start, end):
    pass

def get_k_core_from_graph(graph):
    return nx.k_core(graph)
