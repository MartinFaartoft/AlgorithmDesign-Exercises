import sys, re

class Edge:
	def __init__(self, from_vertex, to_vertex, distance):
		self.from_vertex = from_vertex
		self.to_vertex = to_vertex
		self.distance = distance

class Vertex:
	def __init__(self, name):
		self.name = name
		self.parent = self
		self.children = []

	def union(self, other):
		self.children.append(other)
		other.parent = self
		for child in other.children:
			child.parent = self
			self.children.append(child)
		other.children = []

def parse(filename):
	with open(filename, 'r') as f: data = f.read()
	edge_tuples = re.findall(r'^(.*?)--(.*?) \[(.*?)\].*$', data, re.MULTILINE)
	city_names = [x.strip() for x in re.findall(r'^[^\]]*$', data, re.MULTILINE)[0].split('\n')]
	vertices = {}
	
	for name in city_names:
		vertices[name] = Vertex(name)

	edges = [Edge(vertices[row[0]], vertices[row[1]], int(row[2])) for row in edge_tuples]

	return edges

def kruskal(edges):
	edges.sort(key=lambda x: x.distance)

	dist = 0
	for edge in edges:
		tree1 = edge.from_vertex.parent
		tree2 = edge.to_vertex.parent
		if tree1 == tree2:
			continue
		else:
			if len(tree1.children) > len(tree2.children):
				tree1.union(tree2)
			else:
				tree2.union(tree1)

			dist += edge.distance

	print dist

edges = parse(sys.argv[1])
kruskal(edges)