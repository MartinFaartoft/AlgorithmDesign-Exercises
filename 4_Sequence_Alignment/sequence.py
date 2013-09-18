import sys

def sequence_alignment():
	#TODO: implement alignment algorithm
	pass:

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

seq_data = parse_data()
# for Toy_FASTA.in:
# seq_data = [('Sphinx', 'KQRK'), ('Bandersnatch', 'KAK'), ('Snark', 'KQRIKAAKABK')]

