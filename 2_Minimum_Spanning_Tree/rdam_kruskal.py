import sys, re

class DisjointVertex:
    def __init__(self, name):
        self.name     = name
        self.parent   = self
        self.children = []

    def union(self, vertex):
        # Arrange variables according to who has the most children
        if len(vertex.parent.children) <= len(self.parent.children):
            most_children, least_children = self.parent, vertex.parent
        else:
            most_children, least_children = vertex.parent, self.parent

        most_children.children += least_children.children + [least_children]

        # Path compress
        least_children.parent = most_children
        for child in least_children.children:
            child.parent = most_children

class Edge:
    def __init__(self, first, second, distance):
        self.first = first
        self.second = second
        self.distance = distance

def parse(input_file):
    vertices = {}
    edges = []
    with open(input_file, 'r') as input_file:
        edge_pattern = re.compile('(.*)--(.*) \[(.*)\]')
        for line in input_file:
            line = line.strip()

            # Only have 2 types of lines. If it's not an edge it must be a vertex
            if edge_pattern.match(line):
                groups = edge_pattern.match(line).groups()
                edges.append(Edge(vertices[groups[0]], vertices[groups[1]], int(groups[2])))
            else:
                vertices[line] = DisjointVertex(line)

    return edges

def kruskal(edges):
    edges = sorted(edges, key=lambda edge: int(edge.distance), reverse=True)
    distance = 0

    while edges:
        edge = edges.pop()
        if edge.first.parent != edge.second.parent:
            edge.first.union(edge.second)
            distance += edge.distance

    return distance

edges = parse(sys.argv[1])
print kruskal(edges)