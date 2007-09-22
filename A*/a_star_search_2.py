"""An implementation of the A* searching algorithm.

dyoo@hkn.eecs.berkeley.edu

I got so disgusted at my previous attempt at A*, so here I go again.
Hopefully this version will be easier on the eyes.

A* is a search algorithm that's similar to Dijkstra's algorithm: given
a graph, a start node, and a goal, A* will search for the shortest
path toward the goal.

To help it get there faster, we can provide a heuristic that evaluates
how far we are from that goal.  With a good heuristic, finding an
optimal solution takes MUCH less time.

The main function that one would use is aStar().  Take a look at
_testAStar() to see how it's used.
"""

from priorityqueue import PriorityQueue

def aStar(start, goal, neighbor_func, distance_func, heuristic_func):
    """Returns a sequence of nodes that optmizes for the least cost
    from the start node to the goal.

    Let's describe the data that we pass to this function:

    start: the start of the search.
    goal: the goal of the search.
    neighbor_func: a function that, given a state, returns a list of
                   neighboring states.
    distance_func: a function that takes two nodes, and returns
                   the distance between them.
    heuristic_func: a function that takes two nodes, and returns
                    the heuristic distance between them.

    Each state mush be hashable --- each state must support the
    hash() function.
    """
    pqueue = PriorityQueue()
    g_costs = {start : 1}
    parents = {start : start}
    
    pqueue.push(heuristic_func(start, goal), start)
    while not pqueue.isEmpty():
        next_cost, next_node = pqueue.pop()
        g_costs[next_node] = g_costs[parents[next_node]] \
                             + distance_func(next_node, parents[next_node])
        if next_node == goal: break
        children = neighbor_func(next_node)
        for child in children:
            updateChild(goal, distance_func, heuristic_func,
                        child, next_node, parents, g_costs, pqueue)
    return getPathToGoal(start, goal, parents)

def updateChild(goal, distance_func, heuristic_func,
                child, next_node, parents, g_costs, pqueue):
    """Appropriately update the parents, g_costs, and pqueue structures.

    This is a helper function, since aStar() was getting a bit bulky."""
    if g_costs.has_key(child): return
    f = g_costs[next_node] + distance_func(next_node, child) \
        + heuristic_func(child, goal)
    if pqueue.push(f, child):
        parents[child] = next_node

def getPathToGoal(start, goal, parents):
    """Given the hash of parental links, follow back and return the
    chain of ancestors."""
    try:
        results = []
        while goal != start:
            results.append(goal)
            goal = parents[goal]
        results.append(start)
        results.reverse()
        return results
    except KeyError: return []

def _testGetPathToGoal():
    parents = { 1 : 2,
                2 : 3,
                3 : 4,
                4 : 5 }
    goal = 1
    print getPathToGoal(goal, parents)




######################################################################
###  The rest of this is implementation scaffolding and test stuff.
###  Take a look at it to see how to use this implementation.
######################################################################

class _DistanceDictWrapper:
    """_DistanceDictWrapper is a class wrapper over a dictionary of
    (node1,node2) to distances.  It's set up to make a dictionary look
    like a callable function.  Futhermore, it assumes that distance is
    transitive, so that finding __call__(node1, node2) is the same as
    __call__(node2, node1)."""
    def __init__(self, dict):
        self.dict = dict
    def __call__(self, m, n):
        """Return the distance between m and n.

        Since distance is symmetric, we'll try from m->n, or n->m"""
        if m == n: return 0
        if self.dict.has_key((m, n)):
            return self.dict[(m, n)]
        if self.dict.has_key((n, m)):
            return self.dict[(n, m)]
        return None

class _Neighbor:
    """A quicky class that lets us get the neighbors of a graph,
    given a distance function, and a list of all nodes."""
    def __init__(self, nodes, dist_func):
        self.nodes = nodes
        self.dist_func = dist_func

    def __call__(self, node):
        """Return the neighbors of a node."""
        results = []
        for n in self.nodes:
##            if n == node: continue  # superfluous, since zero
##                                    # is a false value
            if self.dist_func(n, node):	results.append(n)
        print results
        return results
        
def _testAStar():
    """Given the graph:

        3    1
     /-----b----\
    a      |1    d
     \-----c----/
        1     2

    I do a few tests to make sure that A* looks like it works ok.

    Note: as of now, I don't have a heuristic function set up ---
    basically, I'm testing to make sure that it works as Dijkstra's
    algorithm.  If you want to see the heuristic stuff in action, see
    eight_puzzle.py.
    """
    dist_func = _DistanceDictWrapper({('a', 'b') : 3, ('a', 'c') : 1,
                                      ('b', 'c') : 1, ('b', 'd') : 1,
                                      ('c', 'd') : 2})
    nodes = ['a', 'b', 'c', 'd']
    neighbor_func = _Neighbor(nodes, dist_func)
    null_heuristic = lambda x, y: 0

    print "neighbors of a", neighbor_func('a')
    print "neighbors of b", neighbor_func('b')
    print "neighbors of c", neighbor_func('c')
    print "neighbors of d", neighbor_func('d')
    
    print "path from a to d"
    print aStar('a', 'd', neighbor_func, dist_func, null_heuristic)

    print "path from d to a"
    print aStar('d', 'a', neighbor_func, dist_func, null_heuristic)

    print "path from a to a"
    print aStar('a', 'a', neighbor_func, dist_func, null_heuristic)

if __name__ == '__main__':
    _testAStar()
