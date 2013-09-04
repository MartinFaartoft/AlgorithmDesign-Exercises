import sys,re

def parse_data():
	data = sys.stdin.read().splitlines()
	names = filter(re.compile(r'^\d+ .*').search, data)
	prefs = filter(re.compile(r'^\d+:').search, data)
	names = [x[x.find(' ')+1:].strip() for x in names]
	prefs = [x[x.find(':')+2:].split() for x in prefs]
	prefs = map(lambda x: map(lambda y: int(y) -1, x), prefs)
	prefs = zip(range(len(prefs)),prefs)
	return (names, prefs)

def make_women_ranking(prefs):
	d = {}
	for wid,woman_prefer in prefs[1::2]:
		for i,y in enumerate(woman_prefer): 
			d[(wid,y)] = i
	return d

def stable_marriage(prefs,women_ranking):
	married_women = {}
	men = prefs[::2]
	while len(men) != 0:
		man, prefered_women = men[0]
		prefered_woman = prefered_women[0]
		if prefered_woman not in married_women:
			married_women[prefered_woman] = man
			men = men[1::]
		else:
			married_to = married_women[prefered_woman]
			if women_ranking[(prefered_woman, married_to)] > women_ranking[(prefered_woman, man)]:
				married_women[prefered_woman] = man
				men = men[1::]
				men.append(prefs[married_to])
			else:
				men[0] = (man,prefered_women[1::])
	return dict([[v,k] for k,v in married_women.items()])

names,prefs = parse_data()
married_men = stable_marriage(prefs, make_women_ranking(prefs))
for i in range(0,len(married_men)): 
	print names[i*2] + ' -- ' + names[married_men[i*2]]