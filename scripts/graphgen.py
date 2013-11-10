import networkx as nx
import itertools as it

def get_graph_slice(start, end):
    """
    Generate a networkx digraph of the bitcoin data with all transactions
    between start and end
    """
    g_slice = nx.DiGraph()
    with open('user_edges.txt') as fp:
        for line in fp:
            vals = line.split(',')
            if vals[3] < start or vals[3] > end:
                continue
            g_slice.add_edge(vals[1], vals[2], value=float(vals[4]), date=vals[3], transaction_key=int(val[0]))
    return g_slice
