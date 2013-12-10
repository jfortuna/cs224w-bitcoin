import random
import sys
import networkx as nx
from networkx.algorithms import simple_paths
from matplotlib import pyplot as plt
import graphgen
import graphtools
import plot

_MID_WAY_HIGH_BOUND = 500
_MID_WAY_LOW_BOUND = 10

def find_one_many_one(g, margin):
  """ Finds one to many to one instances. First the algorithm identifies
      all structures that match one to many to one structure. Then it 
      ensures that the transaction from start to finish is within an
      acceptable margin. Margin should be a percentage amount that has
      been deducted (ie from 0 to margin percent is seen as laundering)
      This method assumes that a time slice graph has been passed in 
      that ranges from 3 days to one week.
  """
  ys = [0] * (_MID_WAY_HIGH_BOUND - _MID_WAY_LOW_BOUND + 1)
  ins, outs = _build_dict_sets(g)
  starts, ends, total = _find_instances(g, ys, margin, ins, outs)
 # _save_result(range(_MID_WAY_LOW_BOUND, _MID_WAY_HIGH_BOUND+1), ys)
 # _save_nodes(starts, ends)
  _plot_result(range(_MID_WAY_LOW_BOUND, _MID_WAY_HIGH_BOUND+1), ys)
  return total

def _find_instances(g, ys, margin, ins, outs):
  total = 0
  starts = []
  ends = []
  
  for start in g.nodes():
    print 'finished a start node'
    for end in g.nodes():
      if start == end:
        continue
      midways = ins[end].intersection(outs[start])
      if not midways:
        continue
      if _verify_path(g, start, end, midways, margin):
        ys[len(midways)] += 1
        # starts.append(start)
        # ends.append(end)
        total += 1
  return starts, ends, total

def _build_dict_sets(g):
  outs = {}
  ins = {}
  for n in g.nodes():
    ins[n] = set(g.predecessors(n))
    outs[n] = set(g.successors(n))
  return ins, outs


def _verify_path(g, s, e, midways, margin):
  """ Verifying paths requires checking that the money that
      passed into the midways approximately equals the money
      that went into the final location.
  """
  in_sum = 0.0
  out_sum = 0.0

  if len(midways) >= _MID_WAY_LOW_BOUND:
    
    for m in midways:
      for k in g[s][m]:
	in_sum += g[s][m][k]['value']
      for k in g[m][e]:
        out_sum += g[m][e][k]['value']
    
    if out_sum / float(in_sum) <= margin:
      return True
    print 'found a structure, but ignoring'
  return False

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
  p.bar(xs, ys)
  p.set_title("Occurance of X Midway Nodes")
  p.set_xlabel("Number of Midway Nodes")
  p.set_ylabel("Occurance")
  plt.show()


if __name__ == '__main__':
  days = graphgen._days[graphgen._days.index(20110401):]
  # totals = {}
  start = random.choice(days)
  next_index = days.index(start) + 10
  end = days[next_index] if len(days) -1 >= next_index  else days[-1]
  vals = find_one_many_one(graphgen.get_graph_slice(start * graphgen._HMS, end * graphgen._HMS), .04)
  # totals[start] = vals
 
  # plot.plot_frequency_map(totals, title='Money Laundering Instances Over Time',
  #     xlabel='Date', ylabel='Money Laundering Instances', show=True)

