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

def parse_file(inputfile):
    names, preferences, women, men = {}, {}, {}, []
    name_pattern = re.compile("^\d+ ")
    pref_pattern = re.compile("^\d+:")
    with open(inputfile, 'r') as input_file:
        for line in input_file:
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
                men.append(Man(id, names[id], preferences[id]))
    return women, men

def Gale_Shapley(women, bachelors):
    while bachelors:
        bachelor = bachelors.pop()
        womanID = bachelor.preferences.pop()
        new_bachelor = women[womanID].proposed_to_by(bachelor)

        if new_bachelor is not None:
            bachelors.append(new_bachelor)

    # Create pairs
    pairs = []
    for woman in women.values():
        pairs.append((woman.husband, woman))

    return pairs

def print_output(pairs, output):
    pairs = sorted(pairs, key=lambda (husband, wife): husband.id)
    if output is None:  # If no output file is given, print to std.out
        for (husband, wife) in pairs:
            print husband.name + " -- " + wife.name
    else:
        with open(output, 'w') as output_file:
            for (husband, wife) in pairs:
                output_file.write(husband.name + " -- " + wife.name + "\n")

women, men = parse_file(sys.argv[1])
pairs = Gale_Shapley(women, men)

output = None if len(sys.argv) != 3 else sys.argv[2]
print_output(pairs, output)


