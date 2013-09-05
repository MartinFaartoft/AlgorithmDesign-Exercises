import sys,re
REGEX_EDGE_V_A = re.compile(r'^(.*?)--')      # {CATCH}--{IGNORE} [IGNORE]
REGEX_EDGE_V_B = re.compile(r'^.*--(.*?) \[') # {IGNORE}--{CATCH} [IGNORE]
REGEX_EDGE_V_W = re.compile(r'^.* \[(.*?)\]') # {IGNORE}--{IGNORE} [CATCH]

class Vertice(object):
	def __init__(self, name):
		super(Vertice, self).__init__()
		self.name = name
		self.refs = []
		self.parent = self
		self.edges = []

	def join(self, other):
		# Union by rank - CLRS pp. 568
		if len(self.parent.refs) > len(other.parent.refs):
			other.parent.update(self.parent)
		else:
			self.parent.update(other.parent)

	def find_set(self):
		return self.parent

	def update(self, parent):
		for ref in self.refs:
			ref.update(parent)
		self.refs = []
		self.parent = parent
		self.parent.refs.append(self)

def parse_data():
	data = sys.stdin.read().splitlines()
	V = filter(re.compile(r'^((?!--).)*$').search, data)
	V = [v.strip() for v in V]
	V_sets = {}
	for v in V:
		V_sets[v] = Vertice(v)
	E = filter(re.compile(r'^.*--').search, data)
	E = [parse_edge(V_sets, e) for e in E]
	return (V_sets,E)

def parse_edge(V,e):
	e_a = REGEX_EDGE_V_A.findall(e)[0].strip()
	e_b = REGEX_EDGE_V_B.findall(e)[0].strip()
	e_w = int(REGEX_EDGE_V_W.findall(e)[0])
	vertice_a = V[e_a]
	vertice_b = V[e_b]
	return (e_w, (vertice_a, vertice_b))

def kruskal(V,E):
	refs = {}
	cost = 0
	E = sorted(E) # O(E lg(E))
	for edge in E:
		w, (v_a, v_b) = edge
		if v_a.find_set() == v_b.find_set(): 
			continue
		v_a.join(v_b)
		cost += w
	print cost

if __name__ == '__main__':
	V,E = parse_data()
	kruskal(V,E)