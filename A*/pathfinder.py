#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from sys import exit
try:
	from priorityqueue import PriorityQueue
except ImportError:
	print "Cant import PriorityQueue module"
	exit()
	
class Call:
	def __init__(self, plant, start, end):
		self.plant = plant
		self.start = start
		self.end = end
	def __call__(self):
		return getPath(self.start,self.end, astar(self.start, self.end, self.plant))

def astar(start, goal, plant):
	open_list = PriorityQueue()
	close_list = []
	parent = {start:start}
	g_costs = {start:1}
	#metto nella lista open il punto di partenza
	open_list.push(heuristic(start), start)
	#finche la lista open non è vuota
	while not open_list.isEmpty():
		current_cost, current_node = open_list.pop()
		close_list.append(current_node)
		if current_node is goal: break
		#ritorna il vicino e quanto ci vuole per andarci
		for i,v in neighbors(current_node, plant):
			#calcolo il costo totale
			cost = g_costs[current_node] + v
			if i in open_list.popp() and cost < v:
				open_list.remove(i, v)
			elif i not in open_list.popp() and i not in close_list:
				g_costs[i] = cost
				open_list.push(g_costs[i]+heuristic(i), i)
				parent[i] = current_node
	return parent

def getPath(start, goal, parents):
    try:
        results = []
        while goal != start:
            results.append(goal)
            goal = parents[goal]
        results.append(start)
        results.reverse()
        return results
    except KeyError: return []

"""
plant

  b--c
 /   | \
a----e--d
| \ /
g--f

"""

#plant = {('a','b'):14, ('a','f'):14, ('a','g'):10,
#	     ('b','c'):10, ('c','e'):10, ('c','d'):14,
#	     ('e','d'):10, ('e','f'):14, ('f','g'):10, ('a','e'):20}
	     
heuristic = lambda node: 0

def neighbors(node, plant):
	l = []
	for i,v in plant:
		if i is node: l.append((v,plant[i,v]))
		if v is node: l.append((i,plant[i,v]))
	return l
			
#print getPath('a','d',astar('a', 'd'))
