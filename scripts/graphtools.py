import graphgen
import networkx as nx

def get_wccs_from_graph(graph):
    return nx.weakly_connected_components(graph)

def get_wccs_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    return nx.weakly_connected_components(g_slice)

def get_sccs_from_graph(graph):
    return nx.strongly_connected_components(graph)

def get_sccs_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    return nx.strongly_connected_components(graph)


