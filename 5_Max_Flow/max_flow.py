class Edge:
	def __init__(self, start, end, weight, opposite=None):
		if weight <= 0:
			raise ValueError("non-positive weight")

		self.start = start
		self.end = end
		self.weight = weight
		self.initial_capacity = weight
		if not opposite:
			self.opposite = Edge(end, start, weight, self)
		else:
			self.opposite = opposite

	def add_flow(self, flow):
		self.weight -= flow
		self.opposite.weight += flow


def max_flow(edge_dict, source, sink): #map<start_vertex, list<edge>>
	while(True):
		found_path, path = bfs(source, sink, edge_dict)
		if not found_path: 
			break

		augment(edge_dict, path)
	min_cut = path
	#find all edges starting in path, not ending in path, and sum their initial_capacity - that's the max-flow

def augment(edge_dict, path):
	min_flow = min(path, key=lambda x: x.weight)
	for edge in path:
		edge.add_flow(min_flow)

def bfs(source, sink, edge_dict):
	#do breadth first search, and IGNORE all edges with weight 0, treat them as non-existing
	#return tuple (bool, list of edges in path)