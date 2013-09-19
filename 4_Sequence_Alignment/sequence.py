import sys

M = {}

def sequence_alignment(a,b):
	m = len(a)
	n = len(b)

	if (m,n) in M:
		return M[(m,n)]
	
	if m == 0:
		result = n * 6000  # TODO USE BLOSUM DATA
	elif n == 0:
		result = n * 6000  # TODO USE BLOSUM DATA
	else:
		result = min([ 6000 + sequence_alignment(a[:-1], b[:-1]),
					   6000 + sequence_alignment(a[:-1], b),
					   6000 + sequence_alignment(a, b[:-1])
			]) # TODO USE BLOSUM DATA 

	M[(m,n)] = result
	return result
	

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

