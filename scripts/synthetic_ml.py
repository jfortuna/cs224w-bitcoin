import random
import sys
import networkx as nx
from networkx.algorithms import simple_paths
from matplotlib import pyplot as plt
import csv

_NODES = 10000
_EDGES = 25000
_NUM_RUN_THOUGHS = 1
_NUM_ML_CASES = 100
_MID_WAY_LOW_BOUND = 15
_MID_WAY_HIGH_BOUND = 100
_PROBABILITY_REPLACEMENT = .25

def money_laundering():
  """Performs a money laundering test on three different types
     of graphs to test the validity of this method.
  """
  synthetic_graph = nx.gnm_random_graph(_NODES, _EDGES, directed=True)
  nx.write_edgelist(synthetic_graph, 'random_money_launder.edgelist')
  ys_rnd = [0] * (_MID_WAY_HIGH_BOUND - _MID_WAY_LOW_BOUND + 1)
  for i in range(_NUM_RUN_THOUGHS):
    print 'Begin %d Run through out of %d' % (i, _NUM_RUN_THOUGHS - 1)
    gold_key = _add_examples(synthetic_graph)
    _test_graph(synthetic_graph, gold_key, ys_rnd)
    synthetic_graph = nx.read_edgelist('random_money_launder.edgelist', nodetype=int)
  ys_rnd = [y / float(_NUM_RUN_THOUGHS) for y in ys_rnd]

  synthetic_graph = nx.barabasi_albert_graph(NODES, EDGES / NODES)
  nx.write_edgelist(synthetic_graph, 'preferential_money_launder.edgelist')
  ys_pref = [0] * (_MID_WAY_HIGH_BOUND - _MID_WAY_LOW_BOUND + 1)
  for i in range(_NUM_RUN_THOUGHS):
    print 'Begin %d Run through out of %d' % (i, _NUM_RUN_THOUGHS - 1)
    gold_key = _add_examples(synthetic_graph)
    _test_graph(synthetic_graph, gold_key, ys_pref)
    synthetic_graph = nx.read_edgelist('preferential_money_launder.edgelist', nodetype=int)
  ys_pref = [y / float(_NUM_RUN_THOUGHS) for y in ys_pref]
  
  synthetic_graph = nx.watts_strogatz_graph(_NODES, _EDGES / _NODES, _PROBABILITY_REPLACEMENT)
  nx.write_edgelist(synthetic_graph, 'small_world_money_launder.edgelist')
  ys_small = [0] * (_MID_WAY_HIGH_BOUND - _MID_WAY_LOW_BOUND + 1)
  for i in range(_NUM_RUN_THOUGHS):
    print 'Begin %d Run through out of %d' % (i, _NUM_RUN_THOUGHS - 1)
    gold_key = _add_examples(synthetic_graph)
    _test_graph(synthetic_graph, gold_key, ys_small)
    synthetic_graph = nx.read_edgelist('small_world_money_launder.edgelist', nodetype=int)
  ys_small = [y / float(_NUM_RUN_THOUGHS) for y in ys_small]
  
  _save_results(range(_MID_WAY_LOW_BOUND, _MID_WAY_HIGH_BOUND+1), ys_rnd, ys_pref, ys_small)
  _plot_results(range(_MID_WAY_LOW_BOUND, _MID_WAY_HIGH_BOUND+1), ys_rnd, ys_pref, ys_small)

def _test_graph(g, gold, ys):
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
      if len(midways) >= _MID_WAY_LOW_BOUND:
        if gold.get(start) and gold[start].get(end):
          if gold[start][end] > 0:
            gold[start][end] -= 1
            true_pos += 1
            ys[len(midways) - _MID_WAY_LOW_BOUND] += 1
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
  print 'Precision: %s%%' % (true_pos / float(true_pos + false_pos) * 100)
  print 'Recall: %s%%' % (true_pos / float(true_pos + false_neg) * 100)
  print 'Accuracy: %s%%' % ((true_pos + true_neg) / (true_pos + true_neg + false_pos + false_neg) * 100)

def _save_results(xs, yrnd, ypref, ysmall):
  with open('rnd.csv', 'wb') as csvfile:
    freqwriter = csv.writer(csvfile)
    for i in range(len(xs)):
      freqwriter.writerow([xs[i], yrnd[i]])

  with open('pref.csv', 'wb') as csvfile:
    freqwriter = csv.writer(csvfile)
    for i in range(len(xs)):
      freqwriter.writerow([xs[i], ypref[i]])

  with open('small.csv', 'wb') as csvfile:
    freqwriter = csv.writer(csvfile)
    for i in range(len(xs)):
      freqwriter.writerow([xs[i], ysmall[i]])

def _plot_results(xs, yrnd, ypref, ysmall):
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


def _add_examples(g):
  answers = {}
  for i in range(_NUM_ML_CASES):
    n1 = random.choice(g.nodes())
    n2 = random.choice([x for x in g.nodes() if x != n1])
    _update_answers(answers, n1, n2)
    usable = [x for x in g.nodes() if x != n1 or x != n2]
    for j in range(random.randint(_MID_WAY_LOW_BOUND, _MID_WAY_HIGH_BOUND)):
      midway = random.choice(usable)
      usable.remove(midway)
      g.add_edges_from([(n1, midway), (midway, n2)])

  return answers

def _update_answers(d, n1, n2):
  if d.get(n1):
    if d[n1].get(n2):
      d[n1][n2] +=1
    else:
      d[n1][n2] = 1
  else:
    d[n1] = {}
    d[n1][n2] = 1




if __name__ == '__main__':
  money_laundering()
