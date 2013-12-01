import random
import sys
import networkx as nx
from networkx.algorithms import simple_paths
from matplotlib import pyplot as plt


def find_one_many_one(g, money_margin):
  """ Finds one to many to one instances. First the algorithm identifies
      all structures that match one to many to one structure. Then it 
      ensures that the transaction from start to finish is within an
      acceptable margin. Margin should be a percentage amount that has
      been deducted (ie from 0 to margin percent is seen as laundering)
      This method assumes that a time slice graph has been passed in 
      that ranges from 3 days to one week.
  """
  ys = [0] * (_MID_WAY_HIGH_BOUND - _MID_WAY_LOW_BOUND + 1)
  starts, ends = _find_instances(g, ys, margin)
  _save_result(range(_MID_WAY_LOW_BOUND, _MID_WAY_HIGH_BOUND+1), ys)
  _save_nodes(starts, ends)
  _plot_result(range(_MID_WAY_LOW_BOUND, _MID_WAY_HIGH_BOUND+1), ys)

def _find_instances(g, ys, margin):
  total = 0
  starts = []
  ends = []
  for start in g.nodes():
    for end in g.nodes():
      if start == end:
        continue
      paths = simple_paths.all_simple_paths(g, start, end, cutoff=2)
      paths = list(paths)
      if not paths:
        continue
      success, midway = _verify_path(g, paths, margin)
      if success:
        ys[midway - _MID_WAY_LOW_BOUND] += 1
        starts.append(start)
        ends.append(end)
        total += 1
  return starts, ends

def _verify_path(g, paths, margin):
  """ Verifying paths requires checking that the money that
      passed into the midways approximately equals the money
      that went into the final location.
  """
  in_sum = 0.0
  out_sum = 0.0
  num_midway = 0
  for path in paths:
    in_sum += g[path[0]][path[1]]['value']
    out_sum += g[path[1]][path[2]]['value']
    num_midway += 1

  if num_midway >= _MID_WAY_LOW_BOUND:
    if out_sum / float(in_sum) <= margin:
      return True, num_midway
    print 'found a structure, but ignoring'
  return False, _

def _save_result(xs, ys):
  with open('slice_ml.csv', 'wb') as csvfile:
    freqwriter = csv.writer(csvfile)
    for i in range(len(xs)):
      freqwriter.writerow([xs[i], ys[i]])

def _save_nodes(starts, ends):
  with open('ml_nodes.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for s, e in zip(starts, ends):
      writer.writerow([s, e])

def _plot_result(xs, ys):
  fig = plt.figure(1)
  p = fig.add_subplot(111)
  plt.plot(xs, ys, 'b', linewidth=2.0)
  p.set_title("Average Occurance of X Midway Nodes")
  p.set_xlabel("Number of Midway Nodes")
  p.set_ylabel("Average Occurace")
  plt.show()


