import fileinput


class Man:

    def __init__(self, id, name, preferences):
        self.name = name
        self.preferences = map(int, preferences[::-1])
        self.id = int(id)

    def next_woman_on_pref_list(self):
        return self.preferences.pop()


class Woman:

    def __init__(self, name, preferences):
        self.name = name
        self.preferences = {}
        self.husband = None
        for x in range(0, len(preferences)):
            self.preferences[int(preferences[x])] = -x

    def proposed_to_by(self, suitor):
        if self.husband is None:
            self.husband = suitor
        elif self.preferences[self.husband.id] < self.preferences[suitor.id]:
            newly_divorced, self.husband = self.husband, suitor
            return newly_divorced
        else:
            return suitor

# Parsing
names, preferences, women, bachelors = {}, {}, {}, []
status = "Comments"
for line in fileinput.input():
    if status == "Comments":
        if not line.startswith("#"):
            status = "Names"
            continue

    elif status == "Names":
        if line.strip() == "":
            status = "Preferences"
            continue

        lineList = line.split()
        names[int(lineList[0])] = lineList[1].strip()

    elif status == "Preferences":
        lineList = line.split(': ')
        preferences[int(lineList[0])] = lineList[1].strip().split()

for id in names.keys():
    if id % 2 == 0:
        women[id] = Woman(names[id], preferences[id])
    else:
        bachelors.append(Man(id, names[id], preferences[id]))

fileinput.close()

# Actual algorithm
while bachelors:
    bachelor = bachelors.pop()
    womanID = bachelor.next_woman_on_pref_list()

    new_bachelor = women[womanID].proposed_to_by(bachelor)

    if new_bachelor is not None:
        bachelors.append(new_bachelor)

for womanID in women.keys():
    print women[womanID].husband.name + " -- " + women[womanID].name