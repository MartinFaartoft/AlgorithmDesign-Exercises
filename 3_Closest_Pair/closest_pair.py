import sys,re,math
REGEX_EDGE_V_A = re.compile(r'\d')

class Point(object):
    def __init__(self, x, y, id):
        super(Point, self).__init__()
        self.x = x
        self.y = y
        self.id = id

    def distance(self, other):
        return math.sqrt((abs(self.x - other.x)) ** 2 + abs((self.y - other.y)) ** 2)

    def __repr__(self):
        return self.id + ' - ' + str(self.x) + " , " + str(self.y) + "\r\n"

class Pair:
    def __init__(self, p1, p2, dist):
        self.p1 = p1
        self.p2 = p2
        self.dist = dist

    def __repr__(self):
        return str(self.dist)

def smallest_pair(a, b):
    return a if a.dist < b.dist else b


def parse_data():
    data = sys.stdin.read().splitlines()
    dataIndex = data.index("NODE_COORD_SECTION") + 1
    data = data[dataIndex:-1]

    points = []
    for x in data:
        #print x
        if "EOF" in x:
            continue

        x = x.split()
        a = x[0]
        b = float(x[1])
        c = float(x[2])
        points.append(Point(b, c, a))
    return sorted(points, key=lambda p: p.x)

def brute_force(points):
    min_pair = Pair(None, None, float('inf'))
    for i, point_a in enumerate(points):
        for j in range(i+1, len(points)):
            point_b = points[j]
            dist = point_a.distance(point_b)
            if dist < min_pair.dist:
                min_pair = Pair(point_a, point_b, dist)
    return min_pair

def closest_pair(points):
    if len(points) < 4:
        return brute_force(points)

    mid_index = len(points) / 2
    left = points[:mid_index]
    right = points[mid_index:]

    left_pair = closest_pair(left)
    right_pair = closest_pair(right)

    min_pair = smallest_pair(left_pair, right_pair)

    line_x = (left[-1].x + right[0].x) / 2.0
    delta = min_pair.dist
    candidates = sorted(filter(lambda p: p.x > line_x - delta and p.x < line_x + delta, points), key=lambda p: p.y)

    for i, point in enumerate(candidates[:-1]): #skip the last candidate in outer loop. We have compared it to everything already
        next_11 = candidates[i+1:min(len(candidates), i+11)]
        for pair in [Pair(x, point, x.distance(point)) for x in next_11]:
            min_pair = smallest_pair(pair, min_pair)

    return min_pair

print closest_pair(parse_data())