import sys, itertools



def sequence_alignment(a,b):
	m = len(a)
	n = len(b)

	if (m,n) in M:
		return M[(m,n)][0]
	
	if m == 0:
		result = (n * delta, 'base_m')
	elif n == 0:
		result = (m * delta, 'base_n')
	else:
		result = max([ (blosum[a[-1]][b[-1]] + sequence_alignment(a[:-1], b[:-1]), 'match'),
					   (delta + sequence_alignment(a[:-1], b), 'sep_a'),
					   (delta + sequence_alignment(a, b[:-1]), 'sep_b')
			])

	M[(m,n)] = result
	return result[0]
	

def parse_blosum():
	filename = '../../data/BLOSUM62.txt'
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


blosum = parse_blosum()
delta = blosum['A']['*']
seq_data = parse_data()

for ((a_id,a_seq),(b_id, b_seq)) in itertools.combinations(seq_data, 2):
	M = {}
	print a_id, b_id
	print sequence_alignment(a_seq, b_seq)
	if a_id == 'Sphinx' and b_id == 'Bandersnatch':
		for key in M.keys():
			print key, M[key]
	
	#print M[ (len(a_seq), len(b_seq)) ]


def traverse(mem, a_seq, b_seq):
	#get the action from current step

	return traverse( action(a_seq, b_seq) )