import graphgen
import graphtools
import networkx as nx
from networkx.algorithms import simple_paths
import matplotlib.pyplot as plt
import operator

# public trading started at the end of
# April, 2010. This gives a slice beforehand
_START_PUBLIC_TRADING = 20100401*graphgen._HMS

# Ending the search at the end of May gives
# us about a months worth of data after bitcoins
# become tradeable
_END_PUBLIC_TRADING = 20100531*graphgen._HMS

# Announcement date was April 24, 2012
# Start 7 days previously
_START_SATOSHI_DICE = 20120417*graphgen._HMS

# Ending the search 7 days after launch
_END_SATOSHI_DICE = 20120501*graphgen._HMS

# official launch date so nodes
# can be separated to before/after
_LAUNCH_SATOSHI_DICE = 20120424*graphgen._HMS

# Silk Road is known to have launched
# in February 2011. Take all of Februrary
# into consideration
_START_SILK_ROAD = 20110201*graphgen._HMS

# consider half of March as we
# are not sure of the exact launch
# date for the silk road
_END_SILK_ROAD = 20110315*graphgen._HMS

def analyze_public_trading():
    """
    Analyzes the snippet of the graph around the time when bitcoin opened
    for public trading with USD.
    """
    g = graphgen.get_graph_slice(_START_PUBLIC_TRADING, _END_PUBLIC_TRADING)

def analyze_satoshi_dice():
    """ 
    Analyzes the snippet of the bitcoin network around the time that
    SatoshiDice was announced. There is a hard date for its launch.
    """
    g_before = graphgen.get_graph_slice(_START_SATOSHI_DICE, _LAUNCH_SATOSHI_DICE)
    g_after = graphgen.get_graph_slice(_START_SATOSHI_DICE, _END_SATOSHI_DICE)
    before_lcc = graphtools.get_lcc_from_graph(g_before)
    after_lcc = graphtools.get_lcc_from_graph(g_after)
    print len(before_lcc), len(after_lcc)
    '''
    before_in = g_before.in_degree()
    before_in_values = sorted(set(before_in.values()))
    before_in_hist = [before_in.values().count(x)/float(len(g_before.nodes())) for x in before_in_values]
    after_in = g_after.in_degree()
    after_in_values = sorted(set(after_in.values()))
    after_in_hist = [after_in.values().count(x)/float(len(g_after.nodes())) for x in after_in_values]

    plt.loglog(before_in_values, before_in_hist, 'bo', label='In-degree before SatoshiDICE announced')
    plt.loglog(after_in_values, after_in_hist, 'ro', label='In-degree after SatoshiDICE announced')
    plt.legend(loc=1)
    plt.xlabel('Degree')
    plt.ylabel('Fraction of nodes')
    plt.title('In-degree 1 week before and after SatoshiDICE announced')
    plt.show()
    
    before_out = g_before.out_degree()
    before_out_values = sorted(set(before_out.values()))
    before_out_hist = [before_out.values().count(x)/float(len(g_before.nodes())) for x in before_out_values]
    after_out = g_after.out_degree()
    after_out_values = sorted(set(after_out.values()))
    after_out_hist = [after_out.values().count(x)/float(len(g_after.nodes())) for x in after_out_values]

    plt.loglog(before_out_values, before_out_hist, 'bo', label='Out-degree before SatoshiDICE announced')
    plt.loglog(after_out_values, after_out_hist, 'ro', label='Out-degree after SatoshiDICE announced')
    plt.legend(loc=1)
    plt.xlabel('Degree')
    plt.ylabel('Fraction of nodes')
    plt.title('Out-degree 1 week before and after SatoshiDICE announced')
    plt.show()
    '''

    #Can't use k-core with MultiDiGraph
    '''
    g_before.remove_edges_from(g_before.selfloop_edges())
    g_after.remove_edges_from(g_after.selfloop_edges())
    print len(graphtools.get_k_core_from_graph(g_before).nodes())
    print len(graphtools.get_k_core_from_graph(g_after).nodes())
    '''

    #before_node_max_in = graphtools.get_node_max_in_degree(g_before)
    #after_node_max_in = graphtools.get_node_max_in_degree(g_after)
    #print before_node_max_in, after_node_max_in
    #print sorted(g_before.in_degree().iteritems(), key=operator.itemgetter(1))
    #print sorted(g_after.in_degree().iteritems(), key=operator.itemgetter(1))
    #print len(g_after.edges('25', data=True))
    #print nx.get_edge_attributes(g_after, 'transaction_key')
    #print g_after.in_degree(after_node_max_in)
    #new_nodes = set(g_after.in_degree())-set(g_before.in_degree())
    #print len(new_nodes)
    #new_nodes_degrees = {k: g_after.in_degree()[k] for k in new_nodes}
    #print sorted(new_nodes_degrees.iteritems(), key=operator.itemgetter(1))

    time_period = graphgen._days[graphgen._days.index(_START_SATOSHI_DICE/graphgen._HMS):graphgen._days.index(_END_SATOSHI_DICE/graphgen._HMS)]
    transactions_per_day = []
    for day in time_period:
        daystart = int(str(day) + '000000')
        dayend = int(str(day) + '235959')
        transactions = []
        for n, nbrs in g_after.adjacency_iter():
            for nbr, eattr in nbrs.items():
                if (eattr['date'] >= daystart and eattr['date'] <= dayend):
                    transactions.append(1)
        #transactions = [edge for edge in g_after.edges_iter() if (edge['date'] >= daystart and edge['date'] <= dayend)]
        transactions_per_day.append(len(transactions))
    print time_period
    print transactions_per_day
    


def analyze_silk_road():
    """
    Analyzes the snippet of the bitcoin network around the time that
    the silk road launched.
    """
    g = graphgen.get_graph_slice(_START_SILK_ROAD, _END_SILK_ROAD)



"""
  TODO: 
"""
analyze_satoshi_dice()
