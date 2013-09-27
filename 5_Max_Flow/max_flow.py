import Queue, sys

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
		return str(self.start.id) + " --" + str(self.flow) + "/" + str(self.capacity) + "-> " + str(self.end.id)

	def add_flow(self, flow):
		self.flow += flow
		self.opposite.flow -= flow

	def remaining_capacity(self):
		return self.capacity - self.flow


def max_flow(edge_dict, source, sink):
	while(True):
		path, explored = bfs(source, sink, edge_dict)
		if len(path) == 0: 
			break
		augment(edge_dict, path)

	return explored

def augment(edge_dict, path):
	min_flow = min(path, key=lambda x: x.remaining_capacity()).remaining_capacity()
	for edge in path:
		edge.add_flow(min_flow)

def bfs(source, sink, edge_dict):
	explored = {}
	frontier = Queue.Queue()
	frontier.put(source)

	while not frontier.empty():
		vertex = frontier.get()
		explored[vertex.id] = vertex
		for edge in edge_dict[vertex.id]:
			if edge.remaining_capacity() == 0 or edge.end.id in explored:
				continue
			
			if edge.end.id == sink.id:
				edge.end.incoming_edge = edge
				return (make_path(source, sink, explored), explored)
			
			end_vertex = edge.end
			end_vertex.incoming_edge = edge
			frontier.put(end_vertex)
	#no path found, return empty path list
	return ([], explored)
	
def make_path(source, sink, explored):
	path = []
	vertex = sink
	while vertex.id != source.id:
		path.append(vertex.incoming_edge)
		vertex = vertex.incoming_edge.start

	return path

def print_solution(edge_dict, cut):
	bottleneck = []
	v = cut.values()
	for vertex in v:
		bottleneck += filter(lambda e: e.start in v and not e.end in v, edge_dict[vertex.id])

	print "Max flow:\n" + str(sum(map(lambda e: e.flow, bottleneck)))
	print "bottleneck edges: (start --flow/cap-> end)"
	for edge in bottleneck:
		print str(edge)

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


source, sink, edge_dict = parse_data()
cut = max_flow(edge_dict,source,sink)
print_solution(edge_dict, cut)