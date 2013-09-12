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

def parse_data():
	data = sys.stdin.read().splitlines()[6:-1]
	points = []
	for x in data:
		
		x = x.split()
		a = x[0]
		b = float(x[1])
		c = float(x[2])
		points.append(Point(b,c,a))
	return sorted(points, key=lambda p: p.x)

def closest_pair(points):
	if (len(points) < 4):

		min_dist = float('inf')
		for i, point_a in enumerate(points):
			for j in range(i+1, len(points)):
				point_b = points[j]
				dist = point_a.distance(point_b)
				if (dist < min_dist):
					min_point_a = point_a
					min_point_b = point_b
					min_dist = dist
		return (min_point_a, min_point_b, min_dist)

	mid = len(points) / 2 
	left = points[:mid]
	right = points[mid:]

	(l_a, l_b, min_dist_l) = closest_pair(left)
	(r_a, r_b, min_dist_r) = closest_pair(right)

	(min_a, min_b, min_dist) = (l_a, l_b, min_dist_l) if min_dist_l < min_dist_r else (r_a, r_b, min_dist_r)
	
	line_x = (left[-1].x + right[0].x) / 2.0
	delta = min_dist
	candidates = sorted(filter(lambda p: p.x > line_x - delta and p.x < line_x + delta, points), key=lambda p: p.y)

	for i, point in enumerate(candidates):
		if(i+1 == len(candidates)):
			break
		next_11 = candidates[i+1:min(len(candidates), i+11)]
		(dist, (a, b)) = sorted([(x.distance(point), (x, point)) for x in next_11])[0]
		if(dist < min_dist):
			min_dist = dist
			min_a = a
			min_b = b

	return (min_a, min_b, min_dist)
	
	#print min_dist
	#print line_x
	#print candidates

points = parse_data()
print closest_pair(points)



a = Point(8.0,0, "a")
b = Point(3.0,0, "b")
c = Point(6.0,0, "c")
d = Point(11.0,0, "d")
#print closest_pair(sorted([a,b,c,d], key=lambda p: p.x))


