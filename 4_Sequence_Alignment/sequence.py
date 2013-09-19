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
    filename = 'data/BLOSUM62.txt'
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


def traverse(mem, a_seq, b_seq):

    len_a = len(a_seq)
    len_b = len(b_seq)
    if len_a == 0 and len_b == 0:
        return "", ""

    action = mem[(len_a, len_b)][1]

    if action == "match":
        currentA = a_seq[-1]
        currentB = b_seq[-1]
        previous = traverse(mem, a_seq[:-1], b_seq[:-1])
    elif action == "sep_a":
        currentA = a_seq[-1]
        currentB = "-"
        previous = traverse(mem, a_seq[:-1], b_seq)
    else:
        currentA = "-"
        currentB = b_seq[-1]
        previous = traverse(mem, a_seq, b_seq[:-1])

    (prev_a, prev_b) = previous

    now = ((prev_a + currentA), (prev_b + currentB))

    return now

blosum = parse_blosum()
delta = blosum['A']['*']
seq_data = parse_data()

for ((a_id,a_seq),(b_id, b_seq)) in itertools.combinations(seq_data, 2):
    M = {}
    cost = sequence_alignment(a_seq, b_seq)
    print a_id, "(", a_seq, ")",  "--", b_id, "(", b_seq, ")", ":", cost
    (currentA, currentB) = traverse(M, a_seq, b_seq)
    print currentA
    print currentB