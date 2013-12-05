"""The current goals of the methods in this file are to graph
   tags that occur in the bitcoin network. Then, this can be
   expanded to show the evolution of the network over time.
"""

import random
import sys
import networkx as nx
from networkx.algorithms import simple_paths
from matplotlib import pyplot as plt
from utils import save_node_data
import csv



def user_transaction_frequency(g, stamp=''):
  """ Takes in a graph representing a snippet of the bitcoin network
      and graphs a representation of each user's transaction frequency.
      Creates two dicts: one with a frequency mapped to the number of nodes
      with that amount. The other maps a specific node to its frequency.
      The stamp should be something to append to the outputed csv so we know
      which graph snippet the data refers to.
  """
  frequency = {}
  node_to_freq = {}
  for node in g.nodes():
    freq = len(g.neighbors(node))
    frequency[freq] = frequency[freq] + 1 if frequency.get(freq) else 1
    node_to_freq[node] = freq

  save_node_data.save_node_map(node_to_freq, 'node_transaction_freq_'+stamp)
  # plot_node_data.plot_node_map(node_to_freq)
  return frequency


def user_sell_frequency(g, stamp=''):
  """Same as above, but considers in degree, or when the node
     is payed, ie sells something in exchange for bitcoins.
  """
  frequency = {}
  node_to_freq = {}
  for node in g.nodes():
    freq = g.in_degree(node)
    frequency[freq] = frequency[freq] + 1 if frequency.get(freq) else 1
    node_to_freq[node] = freq

  save_node_data.save_node_map(node_to_freq, 'node_sell_freq_'+stamp)
  plot_node_data.plot_node_map(node_to_freq)

def user_buy_frequency(g, stamp=''):
  """Same as first method, but now for the frequency in which a user spends
     money, ie out degree
  """
  frequency = {}
  node_to_freq = {}
  for node in g.nodes():
    freq = g.out_degree(node)
    frequency[freq] = frequency[freq] + 1 if frequency.get(freq) else 1
    node_to_freq[node] = freq

  save_node_data.save_node_map(node_to_freq, 'node_buy_freq_'+stamp)
  plot_node_data.plot_node_map(node_to_freq)



_ROUND_FACTOR = 100 #bitcoin amounts are small, so multiply by a factor, cast to an
                    #int, and then divide
def user_transaction_amount(g, stamp=''):
  """Takes in a graph representing a snippet of the bitcoin network
     and graphs a representation of the amount of bitcoins passing through
     a user. Also maps the frequency of that amount by rounding amounts
     in a specific digit position.

     TODO: decide if it should be spent, recieved, all, or some combination
  """
  amount_frequency = {}
  node_to_amount = {}
  for node in g.nodes():
    total = 0.0
    for e in g.edges(node, data=True):
      total += e['amount']
    node_to_amount[node] = total
    rounded = int(total * _ROUND_FACTOR) / float(_ROUND_FACTOR)
    amount_frequency[rounded] = amount_frequency[rounded] + 1 if \
        amount_frequency.get(rounded) else 1
  save_node_data.save_node_map(node_to_amount, 'node_transaction_amount_'+stamp)
  plot_node_data.plot_node_map(node_to_amount)






