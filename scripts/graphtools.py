import graphgen
import networkx as nx
import numpy as np
from scipy.interpolate import interp1d
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


def get_avg_out_degree_from_graph(graph):
    out_degrees = graph.out_degree()
    return np.mean(out_degrees.values())


def get_avg_out_degree_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    return get_avg_out_degree_from_graph(g_slice)


def get_out_degrees_from_graph(graph):
    return graph.out_degree()


def get_out_degrees_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    return g_slice.out_degree()


def get_num_nodes_edges_from_graph(graph):
    return graph.number_of_nodes(), graph.number_of_edges()


def get_num_nodes_edges_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    return g_slice.number_of_nodes(), g_slice.number_of_edges()


def get_frac_nodes_in_gcc_from_graph(g_slice):
    nodes_in_gcc = len(nx.weakly_connected_components(g_slice)[0])
    return float(nodes_in_gcc) / g_slice.number_of_nodes()


def get_frac_nodes_in_gcc_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    nodes_in_gcc = len(nx.weakly_connected_components(g_slice)[0])
    return float(nodes_in_gcc) / g_slice.number_of_nodes()


def get_effective_diameter_from_dates(start, end):
    g_slice = graphgen.get_graph_slice(start, end)
    return effective_diameter(g_slice)


def get_diameter_from_graph(graph):
    return nx.diameter(graph)


def get_k_core_from_graph(graph):
    return nx.k_core(graph)


def string_to_datetime(string):
    if len(string) == 14:
        return datetime.strptime(string, "%Y%m%d%H%M%S")
    else:
        return datetime.strptime(string, "%Y%m%d")


def calc_gini(x): 
    x = list(x)
    N = len(x)
    x. sort() # increasing order
    G = sum(x[i] * (N-i) for i in range(N)) 
    G = 2.0 * G / (N * sum(x))
    return (1 + 1.0 / N) - G


def effective_diameter(graph, q=0.9):
    if graph.number_of_edges() == 0:
        return 0

    P = nx.floyd_warshall_numpy(graph)
    P[np.diag_indices(P.shape[0])] = np.inf
    paths = np.sort(P[P != np.inf])
    if paths.shape[0] != 0:
        ind = np.floor((paths.shape[0]-1)*q)
        if paths[ind].size == 0:
            return 0
        else:
            return np.mean(paths[ind])
    else:
        return 0

    '''
    nodes = graph.nodes()
    dist = nx.shortest_path_length(graph)
    distances = []
    for node1 in nodes:
        row = []
        for node2 in nodes:
            if node1 == node2:
                row.append(np.inf)
            elif node2 in dist[node1]:
                row.append(dist[node1][node2])
            else:
                row.append(np.inf)
        distances.append(row)
    distances = np.array(distances)
    g_d = [0]
    d = 1
    distances = distances[distances != np.inf]
    total_dyads = distances.size
    if total_dyads:
        while g_d[-1] < q:
            path_counts = len(distances[distances <= d])
            path_frac = path_counts / total_dyads
            g_d.append(path_frac)
            d += 1
        d_range = range(d)
        interpolation = interp1d(g_d, d_range, kind='linear')
        eff_d = interpolation(q)
    else:
        eff_d = 0
    return float(eff_d) / len(nodes)
    '''
