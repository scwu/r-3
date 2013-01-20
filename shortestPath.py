#from __future__ import division
from collections import defaultdict
import MySQLdb as mdb
import sys


def processTime(t):

	if(t == ''):
		return 0;

	#if no minutes
	elif not "min" in t:
		justHours = ""
		for char in t:
			if(char == 'h'):
				break 
			else:
				justHours += char
		return 60*int(justHours)

	else:
		hours = ""
		minutes = ""
		for char in t:
			if(char == 'h'):
				break
			else:
				hours += char

		minutes = t[-5:-3]

		return 60*int(hours) + int(minutes)


def averageValues(origin, destination):
	pro = None
	pro = mdb.connect('localhost', 'root', 'rcubed','test')
	now = pro.cursor(mdb.cursors.DictCursor)
	now.execute("SELECT * FROM trips WHERE origin = %s AND destination = %s", (origin,destination))
	info = now.fetchall()
	sumCost = 0;
	sumTime = 0;

	for i in info:
		sumCost += int(i['cost'][1:])#get rid of dollar sign
		sumTime += processTime(i['time'])

	return ((sumCost)/len(info)), ((sumTime)/len(info))

def calculateWeight(entry, avgC, avgT):
	#import this somehow
	timeWeight = 0.8
	costWeight = 0.2

	entryTime = float(processTime(entry['time']))
	entryCost = float(entry['cost'][1:])

	avgTime = float(avgT)
	avgCost = float(avgC)


	return (costWeight * (entryCost/avgCost)) + (timeWeight * (entryTime/avgTime))

def generateGraph():
	con = None
	try:
		con = mdb.connect('localhost', 'root', 'rcubed', 'test')
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT * FROM Trips")
		data = cur.fetchall()
		v = defaultdict(lambda : defaultdict(str))
		e = defaultdict(lambda : defaultdict(str))

		for d in data:
			avgC, avgT = averageValues(d['origin'], d['destination'])

			if(v[d['origin']][d['destination']] == ''):
				v[d['origin']][d['destination']] = calculateWeight(d, avgC, avgT)
				e[d['origin']][d['destination']] = d['type']
			elif(v[d['origin']][d['destination']] > calculateWeight(d, avgC, avgT)):
				e[d['origin']][d['destination']] = d['type']
				v[d['origin']][d['destination']] = calculateWeight(d, avgC, avgT)
			else:	
				continue #dont do anything

		#print v.keys()
		return v, e

	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		if con:
			con.close()

def initialize(graph, origin):
	d = {} #destination
	p = {} #predecessor
	for node in graph.keys():
		d[node] = 9999
		p[node] = 0
	d[origin] = 0
	return d, p

def relax(node, neighbor, graph, d, p):
	if (d[neighbor] > d[node] + graph[node][neighbor]) :
		d[neighbor] = d[node] + graph[node][neighbor]
		p[neighbor] = node

def bellman_ford(graph, origin):
	d, p = initialize(graph, origin)
	for i in range(len(graph) - 1):
		for u in graph.keys():
			for v in graph[u].keys():
				relax(u, v, graph, d, p)
	return d, p

def getPath(root, leaf, pred):
	if(leaf == root):
		return root
	else:
		return getPath(root, pred[leaf], pred) + "-->" + leaf

def main():
	vertices, edges = generateGraph()
	
	d, p = bellman_ford(vertices, "Philadelphia")

	print p
	path = getPath("Philadelphia", "Seattle", p)

	print path

if __name__ == "__main__":
	main()