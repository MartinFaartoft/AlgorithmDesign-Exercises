import sys, re

from Queue import PriorityQueue

class MyPriorityQueue(PriorityQueue):
	def __init__(self):
		PriorityQueue.__init__(self)
		self.counter = 0

	def put(self, item, priority):
		PriorityQueue.put(self, (priority, self.counter, item))
		self.counter += 1

	def get(self, *args, **kwargs):
		_, _, item = PriorityQueue.get(self, *args, **kwargs)
		return item

class Edge:
	def __init__(self, a, b, distance):
		self.a = a
		self.b = b
		self.distance = distance
		a.edges.append(self)
		b.edges.append(self)

class Vertex:
	def __init__(self, name):
		self.name = name
		self.parent = self
		self.edges = []

def parse(filename):
	with open(filename, 'r') as f: data = f.read()
	edge_tuples = re.findall(r'^(.*?)--(.*?) \[(.*?)\].*$', data, re.MULTILINE)
	city_names = [x.strip() for x in re.findall(r'^[^\]]*$', data, re.MULTILINE)[0].split('\n')]
	vertices = {}
	
	for name in city_names:
		vertices[name] = Vertex(name)

	edges = [Edge(vertices[row[0]], vertices[row[1]], int(row[2])) for row in edge_tuples]

	return (vertices.values())

def add_vertex(vertex, pq, mst, new_edge):
	mst[vertex.name] = True
	for edge in vertex.edges:
		if new_edge and new_edge == edge:
			continue
		pq.put(edge, edge.distance)

def prim(vertices):
	mst = {}
	dist = 0
	pq = MyPriorityQueue()
	
	vertex = vertices[0]
	mst[vertex.name] = True
	add_vertex(vertex, pq, mst, None)
	
	while pq.qsize() > 0:
		edge = pq.get()
		if edge.b.name in mst:
			if edge.a.name in mst:
				continue
			else:
				add_vertex(edge.a, pq, mst, edge)
		else:
			add_vertex(edge.b, pq, mst, edge)
		dist += edge.distance
	print dist

vertices = parse(sys.argv[1])
prim(vertices)