import sys
import networkx as nx
import random
import math

# Control recursion depth
global limit
sys.setrecursionlimit(500000)


def forestFire_mod_burnProcedure(G, node1, node2, myDict, p, r):
    """
    Helper function for forestFire_mod
    Handles burning procedure recursively for the modified Forest Fire model
    Recurive depth is handled by global variable 'limit'
    """
    # Ensure recursion does not go too deep
    global limit
    limit += 1
    if limit >= 5000:
        return
    # Generate a non-zero random floating point between 0 and 1
    z = 0
    while z == 0:
        z = random.random()
    # How many neighbors to "burn"
    x = (int)(math.ceil((math.log10(z) / math.log10(p)) - 1))
    y = (int)(math.ceil((math.log10(z) / math.log10(r*p)) - 1))
    burn = [] # Keep track of which neighbors to burn
    out_nbors = G.successors(node1)
    in_nbors = G.predecessors(node1)
    # No neighbors to burn
    if len(out_nbors) == 0:
        return G
    elif len(in_nbors) == 0:
        return G
    # If there are fewer neighbors than needed to burn, burn all
    elif len(out_nbors) <= x:
        for i in range(0, len(out_nbors)):
            if not myDict.has_key(out_nbors[i]):
                burn.append(out_nbors[i])
                myDict[i] = i
    elif len(in_nbors) <= y:
        for i in range(0, len(in_nbors)):
            if not myDict.has_key(in_nbors[i]):
                burn.append(in_nbors[i])
                myDict[i] = i
    # Choose the 'x' and 'y' amount of neighbors to burn
    else:
        for i in range(0, x):
            a = random.randrange(0, len(out_nbors))
            b = 0
            for j in range(0, i):
                while out_nbors[a] == burn[j] or myDict.has_key(out_nbors[a]):
                    a = random.randrange(0, len(out_nbors))
                    if myDict.has_key(out_nbors[a]):
                        b += 1
                    if (len(out_nbors) - b) < x:
                        break
                if (len(out_nbors) - b) < x:
                    break
            if (len(out_nbors) - b) < x:
                break
            burn.append(out_nbors[a])
            myDict[out_nbors[a]] = out_nbors[a]
        for i in range(0, y):
            a = random.randrange(0, len(in_nbors))
            b = 0
            for j in range(0, i):
                while in_nbors[a] == burn[j] or myDict.has_key(in_nbors[a]):
                    a = random.randrange(0, len(in_nbors))
                    if myDict.has_key(in_nbors[a]):
                        b += 1
                    if (len(in_nbors) - b) < y:
                        break
                if (len(in_nbors) - b) < y:
                    break
            if (len(in_nbors) - b) < y:
                break
            burn.append(in_nbors[a])
            myDict[in_nbors[a]] = in_nbors[a]
    # Burn
    for i in range(0, len(burn)):
        if burn[i] != node2:
            G.add_edge(node2, burn[i])
    # Repeat recursively
    for i in range(0, len(burn)):
        forestFire_mod_burnProcedure(G, burn[i], node2, myDict, p, r)


def gen_forest_fire(n, p, r):
    """
    Generates a graph based on a modified Forest Fire model.
    This is a modified version of the Forest Fire model
    that creates undirected edges in the edge creation process.[1]
    Input:
        n = number of nodes in the graph (integer)
        p = "burn" rate (floating point)
    Output:
        nx.DiGraph()
    """
    # Prepare graph
    G = nx.DiGraph()
    nodeCounter = 0 # Tracks next available node ID
    # Keep adding nodes until we have 'n' nodes
    while nodeCounter < n:
        # Recursion limit
        global limit
        limit = 0
        target = nodeCounter
        G.add_node(target)
        nodeCounter = len(G) # Update next available nodeID
        if nodeCounter == 1:
            continue
        # Select a random node from graph that is not the current 'target' node
        randomNode = random.randrange(0, nodeCounter)
        myDict = dict()
        G.add_edge(randomNode, target)
        myDict[randomNode] = randomNode
        # Start burning
        forestFire_mod_burnProcedure(G, randomNode, target, myDict, p, r)
    return G

