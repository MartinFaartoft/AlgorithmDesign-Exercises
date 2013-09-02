import sys
import re


class Man:
    def __init__(self, id, name, preferences):
        self.name = name
        self.preferences = map(int, preferences[::-1])
        self.id = int(id)


class Woman:
    def __init__(self, name, preferences):
        self.name = name
        self.preferences = {}
        self.husband = None

        for x in range(0, len(preferences)):
            self.preferences[int(preferences[x])] = -x

    def proposed_to_by(self, suitor):
        if self.husband is None or self.preferences[self.husband.id] < self.preferences[suitor.id]:
            newly_divorced, self.husband = self.husband, suitor
            return newly_divorced
        else:
            return suitor

# Parsing
with open(sys.argv[1], 'r') as file:
    names, preferences, women, bachelors = {}, {}, {}, []
    name_pattern = re.compile("^\d+ ")
    pref_pattern = re.compile("^\d+:")

    for line in file:
        if name_pattern.match(line):
            lineList = line.split()
            names[int(lineList[0])] = lineList[1].strip()
        elif pref_pattern.match(line):
            lineList = line.split(': ')
            preferences[int(lineList[0])] = lineList[1].strip().split()

    for id in names.keys():
        if id % 2 == 0:
            women[id] = Woman(names[id], preferences[id])
        else:
            bachelors.append(Man(id, names[id], preferences[id]))

#Actual algorithm
while bachelors:
    bachelor = bachelors.pop()
    womanID = bachelor.preferences.pop()
    new_bachelor = women[womanID].proposed_to_by(bachelor)

    if new_bachelor is not None:
        bachelors.append(new_bachelor)

for woman in women.values():
    print woman.husband.name + " -- " + woman.name