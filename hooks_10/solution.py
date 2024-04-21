from collections import defaultdict
from functools import lru_cache

# Algorithm explanation:
# It's a brute force solution. Back track through every hint. For each hint, check which neighbor sequences would be a valid
# addition to the board.

# After we have all the squares that are neighbors to the hints we can manually complete the remaining squares.

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def go_up_n_lines(count):
	return f"\033[{count}A"

debug = False
n = 9 if not debug else 5
hints = [
	[(0,1), 18], [(0,6), 7], [(1,4), 12], [(2,2), 9], [(2,7), 31], [(4,1), 5], [(4,3), 11],
	[(4,5), 22], [(4,7), 22], [(6,1), 9], [(6,6), 19], [(7,4), 14], [(8,2), 22], [(8,7), 15]
] if not debug else [
	[(0,0), 0], [(1,2), 9], [(1,4), 7], [(2,0), 8], [(3,2), 15], [(3,4), 12], [(4,0), 10]
]
point_to_hint = {h[0]: h[1] for h in hints}
board = defaultdict(list)
digit_to_points = {i:set() for i in range(1, n+1)}
solution_boards = []

def is_valid(p):
	return 0 <= p[0] < n and 0 <= p[1] < n

@lru_cache
def hint_neighbor_count(p):
	return len(get_neighbors(p)) 

@lru_cache
def get_neighbors(p):
	diffs = [(0,1), (1,0), (0,-1), (-1,0)]
	result = [(p[0] + di, p[1] + dj) for (di, dj) in diffs]
	return [p for p in result if is_valid(p)]

@lru_cache
def generate_hint_neighbors(p, target_sum):
	if debug:
		d = {(0,0): [[0,0]], (1,2): [[1,4,0,4]], (1,4): [[4,1,2]], (2,0): [[3,5,0]], (3,2):[[3,5,3,4]], (3,4):[[5,3,4]], (4,0):[[5,5]]}
		return d[p]

	count = hint_neighbor_count(p)
	result = []
	current = []
	def recurse(i=0, current_sum=0):
		if i == count:
			if current_sum == target_sum:
				result.append(current[:])
			return
		for j in range(n+1):
			if current_sum + j > target_sum:
				break
			current.append(j)
			recurse(i+1, current_sum+j)
			current.pop()
	recurse()
	return result

def add_to_board(neighbors, sequence):
	for neighbor, digit in zip(neighbors, sequence):
		board[neighbor].append(digit)
		if digit != 0 and len(board[neighbor]) == 1:
			digit_to_points[digit].add(neighbor)

def remove_from_board(neighbors, sequence):
	for neighbor, digit in zip(neighbors, sequence):
		board[neighbor].pop()
		if digit != 0 and len(board[neighbor]) == 0:
			digit_to_points[digit].remove(neighbor)

def copy_current_board():
	copy = {}
	for e in board:
		if len(board[e]) == 0:
			continue
		copy[e] = [board[e][-1]]
	return copy

def collinear(points):
	i, j = points[0]
	return all(p[0] == i for p in points) or all(p[1] == j for p in points)

def get_line(points):
	return min([p[0] for p in points]), max([p[0] for p in points]), min([p[1] for p in points]), max([p[1] for p in points])

def forms_an_l(digit):
	points = list(digit_to_points[digit])
	if len(points) <= 2:
		return True
	i_min, i_max, j_min, j_max = get_line(points)
	return (all(p[0] == i_min or p[1] == j_min for p in points)
		 or all(p[0] == i_max or p[1] == j_min for p in points)
		 or all(p[0] == i_min or p[1] == j_max for p in points)
		 or all(p[0] == i_max or p[1] == j_max for p in points))

@lru_cache
def contains_intersection(l):
	if len(l) <= 2:
		return False
	seen = set()
	last = None
	for e in l:
		if e == last:
			continue
		if e in seen:
			return True
		seen.add(e)
		last = e

	f = {}
	for e in l:
		if e not in f:
			f[e] = 0
		f[e] += 1
	if len([freq for freq in f.values() if freq > 1]) > 1:
		return True

	return False

def get_row_section(i, j_min, j_max):
	return tuple(board[(i,j)][-1] for j in range(j_min, j_max+1) if len(board[(i,j)]) != 0 and board[(i,j)][-1] != 0)

def get_column_section(j, i_min, i_max):
	return tuple(board[(i,j)][-1] for i in range(i_min, i_max+1) if len(board[(i,j)]) != 0 and board[(i,j)][-1] != 0)

def get_row(i):
	return tuple(board[(i,j)][-1] for j in range(n) if len(board[(i,j)]) != 0 and board[(i,j)][-1] != 0)

def get_column(j):
	return tuple(board[(i,j)][-1] for i in range(n) if len(board[(i,j)]) != 0 and board[(i,j)][-1] != 0)

def passes_line_intersection_criterion(neighbors, sequence):
	return (not any(contains_intersection(get_row(i)) for i in range(n)) and
				not any(contains_intersection(get_column(j)) for j in range(n)))

def passes_maximum_count_criterion():
	for digit in range(1, n+1):
		if len(digit_to_points[digit]) > digit:
			return False
	return True

def passes_l_shape_intersection_criterion_for_digit(digit):
	points = list(digit_to_points[digit])

	if len(points) <= 1 or collinear(points):
		return True # probably true
	
	i_min, i_max, j_min, j_max = get_line(points)
	if all(p[0] == i_min or p[1] == j_min for p in points):
		orientation = 3
		i_row, j_col = i_min, j_min
	elif all(p[0] == i_max or p[1] == j_min for p in points):
		orientation = 0
		i_row, j_col = i_max, j_min
	elif all(p[0] == i_min or p[1] == j_max for p in points):
		orientation = 1
		i_row, j_col = i_min, j_max
	elif all(p[0] == i_max or p[1] == j_max for p in points):
		orientation = 2
		i_row, j_col = i_max, j_max

	i_row
	j_col
	for i in range(i_min, i_max+1):
		if len(board[(i,j_col)]) != 0 and board[(i,j_col)][-1] not in [digit, 0]:
			return False
	for j in range(j_min, j_max+1):
		if len(board[(i_row,j)]) != 0 and board[(i_row,j)][-1] not in [digit, 0]:
			return False
	
	return True

def passes_l_shape_intersection_criterion():
	return all(passes_l_shape_intersection_criterion_for_digit(digit) for digit in range(1, n+1))

def fits_l_shape_in_board(digit):
	points = list(digit_to_points[digit])

	if len(points) <= 1 or collinear(points):
		return True # probably true
	
	i_min, i_max, j_min, j_max = get_line(points)
	if all(p[0] == i_min or p[1] == j_min for p in points):
		orientation = 3
		max_length = min(n - i_min, n - j_min)
	elif all(p[0] == i_max or p[1] == j_min for p in points):
		orientation = 0
		max_length = min(i_max + 1, n - j_min)
	elif all(p[0] == i_min or p[1] == j_max for p in points):
		orientation = 1
		max_length = min(n - i_min, j_max + 1)
	elif all(p[0] == i_max or p[1] == j_max for p in points):
		orientation = 2
		max_length = min(i_max + 1, j_max + 1)
	
	height = i_max - i_min + 1
	width = j_max - j_min + 1

	perimeter = 2 * max_length - 1

	return height <= max_length and width <= max_length and digit <= perimeter

def contains_only_1_type_of_element_inside_and_not_outside(l, i, j):
	l = list(set(l))
	if len(l) == 0:
		return True
	if len(l) > 1:
		return False
	digit = l[0]
	for p in digit_to_points[digit]:
		if p[0] != i and p[1] != j:
			return False
	return True

def passes_valid_partition_criteria():
	def recurse(i_min=0, i_max=n-1, j_min=0, j_max=n-1):
		if i_max - i_min == 0:
			return True

		bottom_left_items = get_row_section(i_max, j_min, j_max) + get_column_section(j_min, i_min, i_max)
		if contains_only_1_type_of_element_inside_and_not_outside(bottom_left_items, i_max, j_min) and recurse(i_min, i_max-1, j_min+1, j_max):
			return True
		
		bottom_right_items = get_row_section(i_max, j_min, j_max) + get_column_section(j_max, i_min, i_max)
		if contains_only_1_type_of_element_inside_and_not_outside(bottom_right_items, i_max, j_max) and recurse(i_min, i_max-1, j_min, j_max-1):
			return True
		
		top_left_items = get_row_section(i_min, j_min, j_max) + get_column_section(j_min, i_min, i_max)
		if contains_only_1_type_of_element_inside_and_not_outside(top_left_items, i_min, j_min) and recurse(i_min+1, i_max, j_min+1, j_max):
			return True
		
		top_right_items = get_row_section(i_min, j_min, j_max) + get_column_section(j_max, i_min, i_max)
		if contains_only_1_type_of_element_inside_and_not_outside(top_right_items, i_min, j_max) and recurse(i_min+1, i_max, j_min, j_max-1):
			return True

		return False
	
	return recurse()


def passes_l_shape_size_criterion():
	return all(fits_l_shape_in_board(digit) for digit in range(1, n+1))

def is_valid_addition(neighbors, sequence):
	if not all(forms_an_l(digit) for digit in range(1, n+1)):
		return False
	
	if not passes_maximum_count_criterion():
		return False

	if not passes_line_intersection_criterion(neighbors, sequence):
		return False

	if not passes_l_shape_size_criterion():
		return False

	if not passes_l_shape_intersection_criterion():
		return False
	
	if not passes_valid_partition_criteria():
		return False

	return True

def print_board():
	for i in range(n):
		for j in range(n):
			if (i,j) in point_to_hint:
				digit = point_to_hint[(i,j)]
				text = f"{bcolors.OKBLUE}{digit:>2}{bcolors.ENDC}"
			elif (i,j) in board and len(board[(i,j)]) > 0:
				digit = board[(i,j)][-1]
				text = f"{digit:>2}" if digit != 0 else "  "
			else:
				text = "  "
			print(text, end=" ")
		print("")

count = [0]
def recurse(i=0):
	count[0] += 1
	if count[0] == 20:
		print_board()
		print("")
		print(go_up_n_lines(n+1), end="")
		count[0] = 0

	if i == len(hints):
		print_board()
		print("(partial) SOLUTION!!!")
		print("")
		solution_boards.append(copy_current_board())
		return
	point, target_sum = hints[i]
	possible_neighbor_sequences = generate_hint_neighbors(point, target_sum)
	for sequence in possible_neighbor_sequences:
		neighbors = get_neighbors(point)

		if any(len(board[neighbor]) > 0 and board[neighbor][-1] != digit for neighbor, digit in zip(neighbors, sequence)):
			continue

		add_to_board(neighbors, sequence)
		if is_valid_addition(neighbors, sequence):
			recurse(i+1)
		remove_from_board(neighbors, sequence)

def get_partial_solutions_intersection():
	board_intersection = {}
	for i in range(n):
		for j in range(n):
			cell_solutions = [b[(i,j)][-1] for b in solution_boards if (i,j) in b]
			if len(set(cell_solutions)) == 1:
				board_intersection[(i, j)] = [cell_solutions[0]]

	print("\n" * (n+3))
	return board_intersection


recurse()

board = get_partial_solutions_intersection()
print_board()
print("intersection of all partial solutions")
print("")



