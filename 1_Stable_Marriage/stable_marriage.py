class Man:
	def __init__(self, name):
		self.name = name
		
class Woman:
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.prefs = {}
	
	def prefers(self, suitor):
		return self.man is None or self.prefs[suitor.id] < self.prefs[self.man.id]

	def accept(self, suitor, men):
		if self.man is not None:
			men.append(self.man)
		self.man = suitor

def solve(men, women):
	while len(men) > 0:
		man = men.pop()
		woman = women[man.prefs.pop()]
		woman.prefers(man) 
			? woman.accept(man, men) 
			: men.push(man)

	for n in women:
		print women[n].man.name + " -- " + women[n].name

def parse(filename):
	men = {}
	women = {}
	f = open(filename, 'r')
	lines = list(f)
	f.close()
	for line in lines:
		line = line.strip()
		if line.startswith('#') or line.startswith('n') or line == '':
			continue
		if ':' in line:
			parse_prefs(line, men, women)
		else:
			parse_person(line, men, women)
	return men.values(), women

def parse_person(line, men, women):
	split = line.split(' ')
	index = int(split[0])
	name = split[-1]
	if index % 2 == 0:
		women[index] = Woman(index, name)
	else:
		men[index] = Man(name)

def parse_prefs(line, men, women):
	split = line.split(':')
	prefs = split[-1].strip()
	index = int(split[0])
	if(index % 2 == 0):
		set_woman_prefs(women[index], prefs)
	else:
		set_man_prefs(men[index], prefs)

def set_man_prefs(man, line):
	man.prefs = [int(i) for i in line.split(' ')]
	man.prefs.reverse()

def set_woman_prefs(woman, line):
	arr = [int(i) for i in line.split(' ')]
	for value, index in enumerate(arr):
		woman.prefs[index] = value

solve(parse('data/stable-marriage-friends.in'))