import sys, re

class Man:
	def __init__(self, id, name):
		self.id = id
		self.name = name
		
class Woman:
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.prefs = {}
		self.man = None
	
	def prefers(self, suitor):
		return self.man is None or self.prefs[suitor.id] < self.prefs[self.man.id]

	def accept(self, suitor):
		bachelor = self.man
		self.man = suitor
		return bachelor

def solve(men, women):
	while len(men) > 0:
		man = men.pop()
		woman = women[man.prefs.pop()]
		if woman.prefers(man):
			bachelor = woman.accept(man) 
			if bachelor is not None:
				men.append(bachelor)
		else: 
			men.append(man)

	for w in sorted(women.values(), key=lambda x: x.man.id):
		print w.man.name + " -- " + w.name

def parse(filename):
	men, women = {}, {}
	with open(filename, 'r') as f:
		data = f.read()
	lines = sorted(re.findall(r'^\d+.*$', data, re.MULTILINE))

	for i in range(0, len(lines), 2):
		parse_person(lines[i].split(' '), men, women)
		parse_prefs(lines[i+1].split(':'), men, women)
		
	return men.values(), women

def parse_person(split, men, women):
	index = int(split[0])
	name = split[-1]
	if index % 2 == 0:
		women[index] = Woman(index, name)
	else:
		men[index] = Man(index, name)

def parse_prefs(split, men, women):
	print(split)
	prefs = split[-1].strip()
	index = int(split[0])
	if(index % 2 == 0):
		arr = [int(i) for i in prefs.split(' ')]
		for value, i in enumerate(arr):
			women[index].prefs[i] = value
	else:
		men[index].prefs = [int(i) for i in prefs.split(' ')]
		men[index].prefs.reverse()

[men, women] = parse(sys.argv[1])
solve(men, women)