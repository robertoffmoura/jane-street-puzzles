from collections import defaultdict
import math

n = 13 # size of the board

grid_expressions = {
	# Row 0
	(0, 4): lambda a, b, c: 6*c - 4*b,

	# Row 1
	(1, 7): lambda a, b, c: 8 - b,

	# Row 2
	(2, 1): lambda a, b, c: (a**b - 4) / (6*c + 1),
	(2, 3): lambda a, b, c: (b + c) / (c - 1),
	(2, 6): lambda a, b, c: b**2 - (b / c),
	(2, 8): lambda a, b, c: math.sqrt(30 + a) / c,
	(2, 10): lambda a, b, c: (a + b) / (c - 3*a),

	# Row 3
	(3, 4): lambda a, b, c: (b - 3*a) / (a - c),
	(3, 7): lambda a, b, c: 8*a - 2*b,
	(3, 9): lambda a, b, c: b / (a - c),
	(3, 11): lambda a, b, c: (b + 9) / math.sqrt(c - a),

	# Row 4
	(4, 1): lambda a, b, c: 18 / (a * c + 1),
	(4, 5): lambda a, b, c: c**b,
	(4, 10): lambda a, b, c: (3 + b**2) / math.sqrt(3 + 2*c),

	# Row 5
	(5, 3): lambda a, b, c: b / (a**2 - c**2),
	(5, 12): lambda a, b, c: math.sqrt(a + 2) / a,

	# Row 6
	(6, 2): lambda a, b, c: a**b - 12 / a,
	(6, 4): lambda a, b, c: 2*c + (c / a),
	(6, 6): lambda a, b, c: 4*a - 5*b,
	(6, 8): lambda a, b, c: c + 2*a,
	(6, 10): lambda a, b, c: b / (9*a - 5*c),

	# Row 7
	(7, 0): lambda a, b, c: (b**3 + 2*c) / (b + 2*c),
	(7, 9): lambda a, b, c: b / (a - 1),

	# Row 8
	(8, 2): lambda a, b, c: (c - b) / (2 * a),
	(8, 7): lambda a, b, c: b / (a - c),
	(8, 11): lambda a, b, c: (b + c) / (a - c),

	# Row 9
	(9, 1): lambda a, b, c: math.log(a, c),
	(9, 3): lambda a, b, c: (c**2 - b) / a,
	(9, 5): lambda a, b, c: (b - 1)**2,
	(9, 8): lambda a, b, c: (43 - a * c)**(1/3) / a,

	# Row 10
	(10, 2): lambda a, b, c: (b - a) / (a - c),
	(10, 4): lambda a, b, c: 11 - b,
	(10, 6): lambda a, b, c: (b - 2*a) / (a - c),
	(10, 9): lambda a, b, c: (c + 3) / a,
	(10, 11): lambda a, b, c: 8*c - (b / c),

	# Row 11
	(11, 5): lambda a, b, c: b**2,

	# Row 12
	(12, 8): lambda a, b, c: (2**b + 1) / (a * c)
}

a, b, c = 0.25, -3, 0.5 # See solve_a_b_c.py

grid = [[None for i in range(n)] for j in range(n)]
result = [[None for i in range(n)] for j in range(n)]

for i in range(n):
	for j in range(n):
		if (i,j) in grid_expressions:
			value = round(grid_expressions[(i,j)](a,b,c))
			grid[i][j] = value

RED = "\033[31m"
RESET = "\033[0m"
def print_board():
	for i in range(n):
		for j in range(n):
			if grid[i][j]:
				print_value = f"{RED}{grid[i][j]:2}{RESET}"
			elif result[i][j]:
				print_value = f"{result[i][j]:2}"
			else:
				print_value = "  "
			print(print_value, end="|")
		print("")

k_to_cells = defaultdict(set)
for i in range(n):
	for j in range(n):
		if grid[i][j]:
			k_to_cells[grid[i][j]].add((i, j))

starting_position = {k:list(k_to_cells[k])[0] for k in k_to_cells}

def is_valid(i,j):
	return 0 <= i < n and 0 <= j < n and result[i][j] is None

directions = [(0,1), (1,0), (0,-1), (-1,0)]
def get_neighbors(i,j):
	return [(i+di,j+dj) for di,dj in directions if is_valid(i+di,j+dj)]

def normalize(b):
	min_i = min(i for i,_ in b)
	min_j = min(j for _,j in b)
	return [(i-min_i, j-min_j) for i,j in b]

def flip(b):
	max_i = max(i for i,_ in b)
	return [(max_i-i, j) for i,j in b]

def rotate(b):
	max_i = max(i for i,_ in b)
	return [(j, max_i-i) for i,j in b]

def translate(a,di,dj):
	return ((i+di,j+dj) for (i,j) in a)

def fits_helper(a,b):
	if len(a) > len(b):
		raise Exception("a must be smaller than b")
	b_max_i = max(i for i,_ in b)
	b_max_j = max(j for _,j in b)
	a_max_i = max(i for i,_ in a)
	a_max_j = max(j for _,j in a)
	b = set(b)
	if (b_max_i - a_max_i + 1) * (b_max_j - a_max_j + 1) < len(a):
		for di in range(b_max_i - a_max_i + 1):
			for dj in range(b_max_j - a_max_j + 1):
				new_a = translate(a,di,dj)
				if all(ai in b for ai in new_a):
					return True
		return False
	else:
		ia,ja = next(iter(a))
		for ib,jb in b:
			new_a = ((i+ib-ia,j+jb-ja) for (i,j) in a)
			if all(ai in b for ai in new_a):
				return True
		return False

def fits(a,b): # returns whether a fits in b
	a = normalize(a)
	b = normalize(b)

	for _ in range(2):
		for i in range(4):
			if fits_helper(a, b):
				return True
			if i < 3:
				a = rotate(a)
		a = flip(a)
	return False

def delete_lines():
	print(f"\033[{n+1}A")

count = [0]
found_solution = [False]
def recurse(k=16,current=[],frontier=[],f_start=0,k_ominos=[]):
	if count[0] == 10000:
		delete_lines()
		print_board()
		count[0] = 0
	count[0] += 1
	if found_solution[0]:
		return
	if k == 0:
		print("SOLUTION!!!")
		print_board()
		print("\n" * n)
		found_solution[0] = True
		return
	if len(current) == 0:
		i,j = starting_position[k]
		current.append((i,j))
		result[i][j] = k
		frontier = get_neighbors(i,j)
		recurse(k,current,frontier,f_start,k_ominos)
		result[i][j] = None
		current.pop()
		return
	if len(current) == k:
		current_set = set(current)
		if not all(cell in current_set for cell in k_to_cells[k]):
			return
		if k < 16 and not fits(current,k_ominos[-1]):
			return
		for k2 in reversed(range(1,k)):
			cells = k_to_cells[k2]
			if not fits(cells,current):
				return
		k_ominos.append(current)
		recurse(k-1,[],[],0,k_ominos)
		k_ominos.pop()
		return
	for f_idx in range(f_start,len(frontier)):
		i,j = frontier[f_idx]
		if grid[i][j] is not None and grid[i][j] != k:
			continue
		current.append((i,j))
		result[i][j] = k
		neighbors = [(ni,nj) for ni,nj in get_neighbors(i,j) if (ni,nj) not in frontier]
		new_frontier = frontier + neighbors
		recurse(k,current,new_frontier,f_idx+1,k_ominos)
		result[i][j] = None
		current.pop()

print("\n" * n)
recurse()
