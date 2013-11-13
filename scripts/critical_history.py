import graphgen
import networkx as nx
from networkx.algorithms import simple_paths
import matplotlib as plt

# public trading started at the end of
# April, 2010. This gives a slice beforehand
_START_PUBLIC_TRADING = 20100401

# Ending the search at the end of May gives
# us about a months worth of data after bitcoins
# become tradeable
_END_PUBLIC_TRADING = 20100531

# Announcement date was April 24, 2012
# Start a week previously
_START_SATOSHI_DICE = 20120417

# Ending the search after a month of
# launch date
_END_SATOSHI_DICE = 20120524

# official launch date so nodes
# can be separated to before/after
_LAUNCH_SATOSHI_DICE = 20120424

# Silk Road is known to have launched
# in February 2011. Take all of Februrary
# into consideration
_START_SILK_ROAD = 20110201

# consider half of March as we
# are not sure of the exact launch
# date for the silk road
_END_SILK_ROAD = 20110315

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

  g = graphgen.get_graph_slice(_START_SATOSHI_DICE, _END_SATOSHI_DICE)


def analyze_silk_road():
  """
    Analyzes the snippet of the bitcoin network around the time that
    the silk road launched.
  """
  g = graphgen.get_graph_slice(_START_SILK_ROAD, _END_SILK_ROAD)



"""
  TODO: 
"""