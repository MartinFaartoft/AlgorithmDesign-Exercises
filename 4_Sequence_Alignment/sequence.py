import sys

def sequence_alignment():
	#TODO: implement alignment algorithm
	pass

def parse_blosum():
	filename = '../data/BLOSUM62.txt'
	with open(filename, 'r') as f: 
		data = f.read().splitlines()[6:]
	chars = data[0].split()
	
	blosum = {char:{} for char in chars}

	for line in data[1:]:
		sub_split = line.split()
		from_char = sub_split[0]
		for index, value in enumerate(sub_split[1:]):
			to_char = chars[index]
			blosum[from_char][to_char] = int(value)

	return blosum


def parse_data():
	data = sys.stdin.read().splitlines()
	seq_data = []
	first = True
	for x in data:
		#x = x.strip()
		if ">" in x:
			if not first:
				seq_data.append((name,seq))
			first = False
			name = x[1: x.index(" ")]
			seq = ""
		else:
			seq += x
	seq_data.append((name,seq))
	return seq_data

parse_blosum()
seq_data = parse_data()
# for Toy_FASTA.in:
# seq_data = [('Sphinx', 'KQRK'), ('Bandersnatch', 'KAK'), ('Snark', 'KQRIKAAKABK')]

