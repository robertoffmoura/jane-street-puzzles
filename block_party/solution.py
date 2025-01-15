debug = False

if not debug:
	n = 9
	region_str = "\n".join([
	"🟨🟨🟪🟦🟦🟪🟪🟪🟦",
	"🟨🟨🟦🟦🟩🟨🟪🟪🟦",
	"🟨🟪🟩🟩🟩🟨🟨🟦🟦",
	"🟦🟪🟩🟦🟩🟦🟨🟪🟪",
	"🟦🟦🟨🟨🟪🟪🟩🟦🟦",
	"🟦🟦🟪🟪🟪🟦🟩🟪🟦",
	"🟨🟦🟩🟩🟨🟨🟪🟪🟪",
	"🟨🟪🟪🟦🟦🟨🟨🟩🟪",
	"🟨🟦🟦🟦🟦🟩🟩🟩🟪"])
else:
	n = 5
	region_str = "\n".join([
	"🟦🟦🟨🟨🟦",
	"🟦🟪🟨🟦🟦",
	"🟪🟪🟨🟪🟨",
	"🟦🟩🟩🟩🟨",
	"🟨🟨🟩🟦🟦"])

print(region_str)
board = [[0 for j in range(n)] for i in range(n)]
solution = [[0 for j in range(n)] for i in range(n)]
region = [list(line) for line in region_str.split("\n") if line != ""]
point_to_region_id = [[-1 for j in range(n)] for i in range(n)]
directions = [(0,1), (1,0), (0,-1), (-1,0)]
hints = set()

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

def get_neighbors(i, j):
	return [(i+di, j+dj) for (di, dj) in directions]

def is_valid(i, j):
	return 0 <= i < n and 0 <= j < n

def set_region_id(i, j, region_id, colour):
	if not is_valid(i, j) or point_to_region_id[i][j] != -1 or region[i][j] != colour:
		return
	point_to_region_id[i][j] = region_id
	for (ni, nj) in get_neighbors(i, j):
		set_region_id(ni, nj, region_id, colour)

def assign_region_ids():
	region_count = 0
	for i in range(n):
		for j in range(n):
			if point_to_region_id[i][j] == -1:
				set_region_id(i, j, region_count, region[i][j])
				region_count += 1
	return region_count

region_count = assign_region_ids()

def get_region_size(region_count):
	region_sizes = [0 for r in range(region_count)]
	for i in range(n):
		for j in range(n):
			region_id = point_to_region_id[i][j]
			region_sizes[region_id] += 1
	return region_sizes

region_size = get_region_size(region_count)
region_seen_count = [[0] * (sz + 1) for sz in region_size]

def format_pos_id_row(row):
	return " ".join(f"{e:2}" for e in row)

def add_to_board(i, j, value):
	board[i][j] = value
	region_id = point_to_region_id[i][j]
	region_seen_count[region_id][value] += 1

def remove_from_board(i, j):
	value = board[i][j]
	board[i][j] = 0
	region_id = point_to_region_id[i][j]
	region_seen_count[region_id][value] -= 1

def nearest_value_of_k_could_be_at_distance_k(i, j, k):
	for distance in range(1, k):
		for di, dj in directions:
			ni, nj = i + di * distance, j + dj * distance
			if not is_valid(ni, nj):
				continue
			if board[ni][nj] == k:
				return False
	for di, dj in directions:
		ni, nj = i + di * k, j + dj * k
		if not is_valid(ni, nj):
			continue
		if board[ni][nj] == 0 or board[ni][nj] == k:
			return True
	return False

def is_valid_addition(i, j, value):
	region_id = point_to_region_id[i][j]
	if region_seen_count[region_id][value] > 1:
		return False
	if not nearest_value_of_k_could_be_at_distance_k(i, j, value):
		return False
	for di, dj in directions:
		for distance in range(1, 7):
			ni, nj = i + di * distance, j + dj * distance
			if not is_valid(ni, nj):
				break
			if board[ni][nj] == distance:
				if not nearest_value_of_k_could_be_at_distance_k(ni, nj, distance):
					return False
	return True

def save_solution():
	for i in range(n):
		for j in range(n):
			solution[i][j] = board[i][j]

def format_grid_element(i, j):
	e = board[i][j]
	text = f"{e:2}" if e > 0 else "  "
	if (i, j) in hints:
		text = f"{bcolors.OKBLUE}{text}{bcolors.ENDC}"
	return text

def print_grid(grid):
	for i in range(n):
		print(" ".join(format_grid_element(i, j) for j in range(n)))

def print_solution():
	print_grid(solution)

def print_board():
	print_grid(board)
	print(f"\033[{n+1}A")

def add_hint(i, j, value):
	add_to_board(i, j, value)
	hints.add((i,j))

print_count = [0]
solution_count = [0]

def backtrack(i = 0, j = 0):
	if j > n - 1:
		j = 0
		i += 1
	
	if i == n:
		save_solution()
		print_solution()
		solution_count[0] += 1
		print("SOLUTION!!!")
		largest_values = get_largest_horizontally_concatenated_number_from_each_region()
		print(" + ".join(str(val) for val in largest_values) + " = " + str(sum(largest_values)))
		print("answer: " + str(sum(largest_values)))
		print("\n\n")
		return
	
	if board[i][j] != 0:
		backtrack(i, j+1)
		return
	
	if print_count[0] == 1e3:
		print_board()
		print_count[0] = 0
	print_count[0] += 1

	region_id = point_to_region_id[i][j]
	sz = region_size[region_id]
	for value in range(1, sz + 1):
		add_to_board(i, j, value)
		if is_valid_addition(i, j, value):
			backtrack(i, j+1)
		remove_from_board(i, j)

def concatenate_number(values):
	current = 0
	for val in values:
		current = 10 * current + val
	return current

def get_concatenated_numbers_by_row(points):
	i_values = list(set(i for (i, j) in points))
	values_by_row = [[board[i][j] for i, j in points if i == i_val] for i_val in i_values]
	return [concatenate_number(values) for values in values_by_row]

def get_largest_horizontally_concatenated_number_from_each_region():
	region_id_to_points = [[] for _ in range(region_count)]
	for i in range(n):
		for j in range(n):
			region_id = point_to_region_id[i][j]
			region_id_to_points[region_id].append((i, j))
	return [max(get_concatenated_numbers_by_row(points)) for points in region_id_to_points]

def main():
	print("region ids:")
	print("\n".join([format_pos_id_row(row) for row in point_to_region_id]))
	print("\n")

	add_hint(1, 4, 2)
	add_hint(4, 1, 4)
	add_hint(4, 7, 1)
	add_hint(7, 4, 1)

	add_hint(0, 2, 1)
	add_hint(3, 3, 1)
	add_hint(3, 5, 1)
	add_hint(5, 5, 1)

	backtrack()
	print("\n" * n)
	print("solution_count:", solution_count[0])

main()