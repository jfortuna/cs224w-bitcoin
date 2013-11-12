import random
import sys
import networkx as nx
from networkx.algorithms import simple_paths
from collections import defaultdict
import matplotlib as plt

NODES = 10000
EDGES = 25000
NUM_RUN_THOUGHS = 1
NUM_ML_CASES = 100
MID_WAY_LOW_BOUND = 15
MID_WAY_HIGH_BOUND = 100
PROBABILITY_REPLACEMENT = .25


def MoneyLaundering():
  synthetic_graph = nx.gnm_random_graph(NODES, EDGES, directed=True)
  nx.write_edgelist(synthetic_graph, 'random_money_launder.edgelist')
  ys_rnd = [] * (MID_WAY_HIGH_BOUND - MID_WAY_LOW_BOUND + 1)
  for i in range(NUM_RUN_THOUGHS):
    print 'Begin %d Run through out of %d' % (i, NUM_RUN_THOUGHS - 1)
    gold_key = AddExamples(synthetic_graph)
    TestGraph(synthetic_graph, gold_key, ys_rnd)
    synthetic_graph = nx.read_edgelist('random_money_launder.edgelist', nodetype=int)
  ys_rnd = [y / float(NUM_RUN_THOUGHS) for y in ys_rnd]

  synthetic_graph = nx.barabasi_albert_graph(NODES, EDGES / NODES)
  nx.write_edgelist(synthetic_graph, 'preferential_money_launder.edgelist')
  ys_pref = [] * (MID_WAY_HIGH_BOUND - MID_WAY_LOW_BOUND + 1)
  for i in range(NUM_RUN_THOUGHS):
    print 'Begin %d Run through out of %d' (i, NUM_RUN_THOUGHS - 1)
    gold_key = AddExamples(synthetic_graph)
    TestGraph(synthetic_graph, gold_key, ys_pref)
    synthetic_graph = nx.read_edgelist('preferential_money_launder.edgelist', nodetype=int)
  ys_pref = [y / float(NUM_RUN_THOUGHS) for y in ys_pref]
  
  synthetic_graph = nx.watts_strogatz_graph(NODES, EDGES / NODES, PROBABILITY_REPLACEMENT)
  nx.write_edgelist(synthetic_graph, 'small_world_money_launder.edgelist')
  ys_small = [] * (MID_WAY_HIGH_BOUND - MID_WAY_LOW_BOUND + 1)
  for i in range(NUM_RUN_THOUGHS):
    print 'Begin %d Run through out of %d' (i, NUM_RUN_THOUGHS - 1)
    gold_key = AddExamples(synthetic_graph)
    TestGraph(synthetic_graph, gold_key, ys_pref)
    synthetic_graph = nx.read_edgelist('small_world_money_launder.edgelist', nodetype=int)
  ys_small = [y / float(NUM_RUN_THOUGHS) for y in ys_small]
  
  PlotResults(range(MID_WAY_LOW_BOUND, MID_WAY_HIGH_BOUND+1), ys_rnd, ys_pref, ys_small)

def TestGraph(g, gold, ys):
  print 'Starting to Calculate Statistics'
  true_pos = 0
  false_pos = 0
  true_neg = 0
  false_neg = 0 #will always be zero, because we always consider ones bigger than the estimate
  print 'RESULTS'
  for start in g.nodes():
    for end in g.nodes():
      if start == end:
        continue
      paths = simple_paths.all_simple_paths(g, start, end, cutoff=2)
      paths = list(paths)
      if not paths:
        continue
      midways = []
      for path in paths:
        midways.append(path[1])
      if len(midways) >= MID_WAY_LOW_BOUND:
        if gold.get(start) and gold[start].get(end):
          if gold[start][end] > 0:
            gold[start][end] -= 1
            true_pos += 1
            ys[len(midways)] += 1
          else:
            false_pos -= 1
        else:
          false_pos += 1
      elif gold.get(start) and gold[start].get(end) and gold[start][end] >0:
        false_neg += 1
      else:
        true_neg += 1
  print 'True Positives: %s\nTrue Negatives: %s, False Positives: %s, False Negatives: %s' % (
      true_pos, true_neg, false_pos, false_neg)
  print 'Precision: %s' % (true_pos / float(true_pos + false_pos))
  print 'Recall: %s' % (true_pos / float(true_pos + false_neg))
  print 'Accuracy: %s' % ((true_pos + true_neg) / (true_pos + true_neg + false_pos + false_neg))

def PlotResults(xs, yrnd, ypref, ysmall):
  fig = plt.figure(1)
  p = fig.add_subplot(111)
  plt.plot(xs, yrnd, 'b', linewidth=2.0, label='Random Graph')
  plt.plot(xs, ypref, 'r', linewidth=2.0, label='Preferential Graph')
  plt.plot(xs, ysmall, 'g', linewidth=2.0, label='Small World Graph')
  p.legend()
  p.set_title("Average Occurance of X Midway Nodes")
  p.set_xlabel("Number of Midway Nodes")
  p.set_ylabel("Average Occurace")
  plt.show()


def AddExamples(g):
  answers = {}
  for i in range(NUM_ML_CASES):
    n1 = random.choice(g.nodes())
    n2 = random.choice([x for x in g.nodes() if x != n1])
    UpdateAnswers(answers, n1, n2)
    usable = [x for x in g.nodes() if x != n1 or x != n2]
    for j in range(random.randint(MID_WAY_LOW_BOUND, MID_WAY_HIGH_BOUND)):
      midway = random.choice(usable)
      usable.remove(midway)
      g.add_edges_from([(n1, midway), (midway, n2)])

  return answers

def UpdateAnswers(d, n1, n2):
  if d.get(n1):
    if d[n1].get(n2):
      d[n1][n2] +=1
    else:
      d[n1][n2] = 1
  else:
    d[n1] = {}
    d[n1][n2] = 1




if __name__ == '__main__':
  MoneyLaundering()
