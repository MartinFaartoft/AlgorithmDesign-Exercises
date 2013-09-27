import Queue
import sys

class Vertex:
	def __init__(self, id):
		self.id = id


class Edge:
	def __init__(self, start, end, capacity, opposite=None):
		if capacity <= 0:
			raise ValueError("non-positive capacity")

		self.start = start
		self.end = end
		self.flow = 0
		self.capacity = capacity
		if not opposite:
			self.opposite = Edge(end, start, capacity, self)
		else:
			self.opposite = opposite

	def __repr__(self):
		return str(self.start.id) + " -- " + str(self.flow) + " -> " + str(self.end.id)

	def add_flow(self, flow):
		self.flow += flow
		self.opposite.flow -= flow

	def remaining_capacity(self):
		return self.capacity - self.flow



def max_flow(edge_dict, source, sink): #map<start_vertex, list<edge>>
	while(True):
		found_path, path, explored_vertices = bfs(source, sink, edge_dict)
		if not found_path: 
			break

		augment(edge_dict, path)
	min_cut = explored_vertices
	return min_cut
	#find all edges starting in path, not ending in path, and sum their initial_capacity - that's the max-flow

def augment(edge_dict, path):
	min_flow = min(path, key=lambda x: x.remaining_capacity())
	for edge in path:
		edge.add_flow(min_flow.remaining_capacity())

def bfs(source, sink, edge_dict):
	explored_vertices = {}

	frontier = Queue.Queue()
	frontier.put(source)
	while not frontier.empty():
		vertex = frontier.get()
		explored_vertices[vertex.id] = vertex
		for edge in edge_dict[vertex.id]:
			if edge.remaining_capacity() == 0 or edge.end.id in explored_vertices:
				continue
			if edge.end.id == sink.id:
				edge.end.incoming_edge = edge
				return (True, make_path(source, sink, explored_vertices), explored_vertices)
			end_vertex = edge.end
			end_vertex.incoming_edge = edge
			frontier.put(end_vertex)
	return (False, [], explored_vertices)
	#do breadth first search, and IGNORE all edges with remaining_capacity == 0, treat them as non-existing
	#return tuple (bool, list of edges in path, list of vertices explored)

def make_path(source, sink, explored_vertices):
	path = []
	vertex = sink
	while vertex.id != source.id:
		path.append(vertex.incoming_edge)
		vertex = vertex.incoming_edge.start

	return path

def parse_data():
	data = sys.stdin.read().splitlines()
	num_vertices = int(data[0])
	vertices = {}
	for i in xrange(num_vertices):
		name = data[i+1]
		vertices[i] = Vertex(i)
	num_edges = int(data[num_vertices + 1 ])
	edge_dict = {}
	for i in xrange(num_edges):
		edge_dict[i] = [] 
	for i in xrange(num_edges):
		line = map(lambda x: int(x) , data[i + num_vertices + 2].split())
		v1 = vertices[line[0]]
		v2 = vertices[line[1]]
		cap = line[2]
		if (cap == -1):
			cap = float("inf")
		edge = Edge(v1, v2, cap)

		edges = edge_dict[v1.id]
		edges.append(edge)
		edge_dict[v1] = edges

		edges = edge_dict[v2.id]
		edges.append(edge.opposite)
		edge_dict[v2] = edges
	return (vertices[0], vertices[num_vertices-1], edge_dict)

def print_solution(edge_dict, cut):
	cap = 0
	vertices = cut.values()
	for vertex in vertices:
		edges = edge_dict[vertex.id]
		for edge in edges:
			if edge.start in vertices:
				if edge.capacity == (float("inf")):
					break
				cap += edge.capacity
	print cap



v1 = Vertex(1)
v2 = Vertex(2)
#v3 = Vertex(3)

e1 = Edge(v1, v2, 10)
#e2 = Edge(v2, v3, 10)

edge_dict = {}
edge_dict[v1.id] = [e1]
edge_dict[v2.id] = [e1.opposite]
#edge_dict[v3.id] = [e2.opposite]

#max_flow(edge_dict, v1, v2)
(source, sink, edge_dict) = parse_data()
cut = max_flow(edge_dict,source,sink)
print_solution(edge_dict, cut)

