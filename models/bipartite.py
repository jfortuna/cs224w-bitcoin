

import networkx as nx
from networkx.algorithms import bipartite

ACTOR = 0
SOCIETY = 1

def assemble_actors_and_societies(g, ratio):
  """ Returns a bipartite graph consisting of actors and societies based on the given
      ratio of in degree to out degree. ie if the ratio is 2, then there must be 2 
      in edges for every out edge in order to qualify as a society.
  """
  in_degrees = g.in_degree()
  out_degrees = g.out_degree()
  B = nx.Graph()
  for key in in_degrees:
    if not out_degree.get():
      B.add_node(key, bipartite=SOCIETY)
    elif in_degrees[key] / float(out_degrees[key]) >= ratio:
      B.add_node(key, bipartite=SOCIETY)
    else:
      B.add_node(key, bipartite=ACTOR)
  for n1, n2 in g.edges():
    if B[n1]['bipartite'] != B[n2]['bipartite']:
      B.add_edge(n1,n2)
  return B

  
def sim_rank_analysis(g, c=.6, k=5):
  """ Performs sim rank analysis on the given graph.
  """
  rk = _simrank_k0(g)
  for _ in range(K - 1):

    rk_new = _one_itr_simrank(g, rk, c)
    if _converges(rk, rk_new):
      break
    rk = rk_new

def _converges(old, new, diff=1e-4):
  for k in old:
    if abs(old[k] - new[k]) > diff:
      return False
  return True


def _simrank_k0(g):
  rk = {}
  for n1 in g.nodes():
    for n2 in g.nodes():
      rk[(n1,n2)] = 1 if n1 == n2 else 0
  return rk

def _one_itr_simrank(g, prev, c):
  rk = {}
  for n1 in g.nodes():
    for n2 in g.nodes():
      if n1 == n2:
        rk[(n1, n2)] = 1
      elif g.in_degree(n1) == 0 or g.in_degree(n2) == 0:
        rk[(n1, n2)] = 0
      else:
        rk[(n1,n2)] = c / float(g.in_degree(n1) * g.in_degree(n2)) \
            * _sum_ranks(g, n1, n2, prev)
  return rk

def _sum_ranks(g, n1, n2, prev):
  total = 0.0
  for p1 in g.predecessors(n1):
    for p2 in g.predecessors(n2):
      total += prev[(p1, p2)]
  return total

def salsa_analysis(g):
  """ Performs SALSA analysis on the given graph. This requires first splitting
      the graph into a bipartite graph (which is referenced in the SALSA paper)

      TODO (ben): help me understand how to use the Markov chains as discussed
      in the paper
  """
  B = _salsa_bipartite(g)


def _salsa_bipartite(g):
  B = nx.Graph()
  visited = set()
  for n in g.nodes():
    if n in visited:
      continue
    visited.add(n)
    if g.in_degree(n) > 0:
      B.add_node(str(n)+'s', bipartite=SOCIETY)
    if g.out_degree(n) > 0:
      B.add_node(str(n)+'a', bipartite=ACTOR)
    for neighbor in g.neighbors(n):
      if neighbor in visited:
        continue
      visited.add(neighbor)
      neighbors = []
      if g.in_degree(neighbor) > 0:
        B.add_node(str(neighbor)+'s', bipartite=SOCIETY)
        if B.get_node(str(n)+'a'):
          B.add_edge(str(n)+'a', str(neighbor)+'s')
      if g.out_degree(neighbor) > 0:
        B.add_node(str(neighbor)+'a', bipartite=ACTOR)
        if B.get_node(str(n)+'s'):
          B.add_edge(str(neighbor)+'a', str(n)+'s')
  return B
