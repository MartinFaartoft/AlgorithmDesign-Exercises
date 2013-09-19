import sys, itertools



def sequence_alignment(a,b):
	m = len(a)
	n = len(b)

	if (m,n) in M:
		return M[(m,n)]
	
	if m == 0:
		result = n * delta  # TODO USE BLOSUM DATA
	elif n == 0:
		result = n * delta  # TODO USE BLOSUM DATA
	else:
		result = max([ blosum[a[-1]][b[-1]] + sequence_alignment(a[:-1], b[:-1]),
					   delta + sequence_alignment(a[:-1], b),
					   delta + sequence_alignment(a, b[:-1])
			]) # TODO USE BLOSUM DATA 

	M[(m,n)] = result
	return result
	

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


