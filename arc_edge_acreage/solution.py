import math

def solution(m, n):
	# The idea behind the solution is that a region of area 32 can be
	# represented as a fixed polyomino of 16 squares placed diagonally
	# inside the grid. We then calculate the perimeter of each polyomino
	# and choose half of the sides of the polyomino to be concave 
	# quarter-circle segments and the other half to be convex 
	# quarter-circle segments.
	count = [0]
	polyomino = []
	untried_set = [(0,0)]
	polyomino_neighbors = set()
	perimeter_count = {}

	# We could use a stack to keep track of the max and min values
	# so that getting these values would be O(1) instead of O(n).
	# Using stacks we'd add the new max and min values to each stack
	# whenever a square is added to the current polyomino, and pop 
	# from the stack when the square is popped from the polyomino.
	# Because there are only 232 polyominos that fit in the grid,
	# this optimisation is not necessary.
	def get_max_sum(): 
		return max([y + x for x,y in polyomino])
	
	def get_min_sum():
		return min([y + x for x,y in polyomino])
	
	def get_max_diff():
		return max([y - x for x,y in polyomino])
	
	def get_min_diff():
		return min([y - x for x,y in polyomino])

	def get_neighbors(square):
		x, y = square
		neighbors = []
		for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
			if y + dy < 0 or (y + dy == 0 and x + dx < 0):
				continue
			s = (x + dx, y + dy)
			if s not in polyomino_neighbors and s not in polyomino:
				neighbors.append(s)
		return neighbors
	
	def new_polyomino_fits_inside_grid(new_square):
		x, y = new_square
		if len(polyomino) > 0:
			new_max_sum = max(get_max_sum(), y + x)
			new_min_sum = min(get_min_sum(), y + x)
			new_max_diff = max(get_max_diff(), y - x)
			new_min_diff = min(get_min_diff(), y - x)
			if new_max_sum - new_min_sum + 2 > m or new_max_diff - new_min_diff + 2 > m:
				return False
		return True
	
	def is_simple_closed_curve(polyomino):
		# Returns true if the polyomino has no holes.

		# How many times each vertex appears.
		vertex_count = {}
		for x, y in polyomino:
			for vx, vy in [(0,0), (1,0), (0,1), (1,1)]:
				vertex = x + vx, y + vy
				if vertex not in vertex_count:
					vertex_count[vertex] = 0
				vertex_count[vertex] += 1
		interior_points = sum([1 for vertex,c in vertex_count.items() if c == 4])
		boundary_points = sum([1 for vertex,c in vertex_count.items() if c in [1,2,3]])
		# Prick's theorem
		holes = n + 1 - interior_points - boundary_points//2
		return holes == 0
	
	def get_positions():
		# if the diagonally bounding rectangle of a polyomino is smaller than the grid,
		# it can be placed in multiple positions. For example, a (2, 3) rectangle fits 
		# inside a (4, 4) square in 3 * 2 = 6 positions because there are 3 rows to 
		# choose and 2 columns to choose where to place the rectangle.
		return (m - (get_max_sum() - get_min_sum() + 1)) * (m - (get_max_diff() - get_min_diff() + 1))

	def redelmeier_recursion(untried_set):
		while len(untried_set) > 0:
			new_square = untried_set.pop()
			if not new_polyomino_fits_inside_grid(new_square):
				continue
			if len(polyomino) == n - 1:
				polyomino.append(new_square)
				if not is_simple_closed_curve(polyomino):
					polyomino.pop()
					continue
				count[0] += 1
				positions = get_positions()
				p = get_perimeter(polyomino)
				if p not in perimeter_count:
					perimeter_count[p] = 0
				perimeter_count[p] += positions
				print("polyomino", polyomino)
				print("sum", get_min_sum(), get_max_sum())
				print("diff", get_min_diff(), get_max_diff())
				print("positions", positions)
				print("perimeter", p)
				print_polyomino(polyomino)
				print("")
				polyomino.pop()
				continue
			new_untried_set = untried_set.copy()
			new_neighbors = get_neighbors(new_square)
			new_untried_set.extend(new_neighbors)
			for s in new_neighbors:
				polyomino_neighbors.add(s)
			polyomino.append(new_square)
			redelmeier_recursion(new_untried_set)
			polyomino.pop()
			for s in new_neighbors:
				polyomino_neighbors.remove(s)

	redelmeier_recursion(untried_set)
	print("frequency of polyomino perimeters", perimeter_count)
	answer = 0
	for perimeter, c in perimeter_count.items():
		answer += c * math.comb(perimeter, perimeter//2)
	print("answer:", answer)
	return

def print_polyomino(l):
	min_x, min_y = float("inf"), float("inf")
	max_x, max_y = float("-inf"), float("-inf")
	for x, y in l:
		min_x = min(min_x, x)
		min_y = min(min_y, y)
		max_x = max(max_x, x)
		max_y = max(max_y, y)
	result = [["  " for x in range(min_x, max_x+1)] for y in range(min_y, max_y+1)]
	for x,y in l:
		result[max_y - (y - min_y)][x - min_x] = "🟩"
	print("\n".join(["".join(row) for row in result]))

def get_perimeter(polyomino):
	perimeter = 0
	for x, y in polyomino:
		for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
			if (x+dx, y+dy) not in polyomino:
				perimeter += 1
	return perimeter

m = 7
n = 16
solution(m, n)
