n = 10

region_str = """
🟨🟨🟨🟨🟦🟦🟦🟦🟦🟦
🟨🟦🟦🟨🟦🟦🟦🟦🟦🟪
🟨🟦🟩🟩🟩🟩🟩🟪🟪🟪
🟨🟦🟦🟩🟩🟩🟩🟩🟨🟪
🟪🟦🟦🟦🟦🟦🟩🟪🟨🟨
🟪🟪🟨🟦🟨🟪🟪🟪🟨🟨
🟪🟨🟨🟩🟨🟨🟨🟪🟪🟪
🟪🟨🟩🟩🟨🟪🟨🟪🟨🟨
🟪🟨🟨🟩🟪🟪🟨🟨🟨🟨
🟪🟩🟩🟩🟩🟪🟪🟨🟨🟨
"""

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

print(region_str)
hint_to_point = {}
point_to_hint = {}
board = [[0 for j in range(n)] for i in range(n)]
solution = [[0 for j in range(n)] for i in range(n)]

region = [list(line) for line in region_str.split("\n") if line != ""]

pos_id = [[-1 for j in range(n)] for i in range(n)]
directions = [(0,1), (1,0), (0,-1), (-1,0)]
knight_directions = [(1,2), (2,1), (-1,2), (2,-1), (1,-2), (-2,1), (-1,-2), (-2,-1)]

def get_neighbors(i, j):
	return [(i+di, j+dj) for (di, dj) in directions]

def get_knight_neighbors(i, j):
	return [(i+di, j+dj) for (di, dj) in knight_directions]

def is_valid(i, j):
	return 0 <= i < n and 0 <= j < n

def set_region_id(i, j, region_id, colour):
	if not is_valid(i, j) or pos_id[i][j] != -1 or region[i][j] != colour:
		return
	pos_id[i][j] = region_id
	for (ni, nj) in get_neighbors(i, j):
		set_region_id(ni, nj, region_id, colour)

def assign_region_ids():
	region_count = 0
	for i in range(n):
		for j in range(n):
			if pos_id[i][j] == -1:
				set_region_id(i, j, region_count, region[i][j])
				region_count += 1
	return region_count

region_count = assign_region_ids()

def format_pos_id_row(row):
	return " ".join(f"{e:2}" for e in row)

print("region ids:")
print("\n".join([format_pos_id_row(row) for row in pos_id]))
print("\n")

row_visits = [0 for i in range(n)]
col_visits = [0 for j in range(n)]
region_visits = [0 for i in range(region_count)]

board_capacity = 60 # lowest common multiple of n and region_count

def is_valid_addition(i, j):
	region_id = pos_id[i][j]
	return (region_visits[region_id] <= board_capacity // region_count
			and row_visits[i] <= board_capacity // n
			and col_visits[j] <= board_capacity // n)

def add_to_board(i, j, value):
	if (i, j) in point_to_hint:
		return
	board[i][j] = value
	row_visits[i] += 1
	col_visits[j] += 1
	region_id = pos_id[i][j]
	region_visits[region_id] += 1

def remove_from_board(i, j):
	if (i, j) in point_to_hint:
		return
	board[i][j] = 0
	row_visits[i] -= 1
	col_visits[j] -= 1
	region_id = pos_id[i][j]
	region_visits[region_id] -= 1

def add_hint(i, j, hint):
	add_to_board(i, j, hint)
	hint_to_point[hint]	= (i, j)
	point_to_hint[(i, j)] = hint

add_hint(0, 0, 1)
add_hint(2, 1, 4)
add_hint(3, 5, 7)
add_hint(4, 9, 10)
add_hint(1, 9, 13)
add_hint(4, 5, 16)
add_hint(7, 3, 19)
add_hint(9, 2, 22)
add_hint(8, 2, 25)
add_hint(5, 4, 28)
add_hint(5, 9, 31)
add_hint(5, 8, 34)
add_hint(8, 8, 37)
add_hint(2, 9, 40)
add_hint(0, 6, 43)
add_hint(3, 2, 46)
add_hint(6, 0, 49)

def save_solution():
	for i in range(n):
		for j in range(n):
			solution[i][j] = board[i][j]

def print_grid(grid):
	for i in range(n):
		for j in range(n):
			digit = grid[i][j]
			if (i,j) in point_to_hint:
				text = f"{bcolors.OKBLUE}{digit:>3}{bcolors.ENDC}"
			else:
				text = f"{digit:>3}" if digit > 0 else "   "
			print(text, end="")
		print("")

def print_solution():
	print_grid(solution)

def print_board():
	print_grid(board)
	print(f"\033[{n+1}A")

def is_valid_board():
	total = sum(row_visits)
	if not all(visits == total // n for visits in row_visits):
		return False
	if not all(visits == total // n for visits in col_visits):
		return False
	if not all(visits == total // region_count for visits in region_visits):
		return False
	return True

print_count = [0]

def backtrack(number = 1, i = 0, j = 0):
	if number in hint_to_point:
		if hint_to_point[number] != (i, j):
			return
	
	if board[i][j] != 0 and board[i][j] != number:
		return
	
	if print_count[0] == 1e4:
		print_board()
		print_count[0] = 0
	print_count[0] += 1

	add_to_board(i, j, number)

	if number == board_capacity:
		if is_valid_board():
			save_solution()
			print_solution()
			print("SOLUTION!!!")
			print("")
		remove_from_board(i, j)
		return

	if is_valid_addition(i, j):
		for (ni, nj) in get_knight_neighbors(i, j):
			if not is_valid(ni, nj) or pos_id[ni][nj] == pos_id[i][j]:
				continue
			backtrack(number + 1, ni, nj)
	remove_from_board(i, j)

def dfs(i, j, seen):
	if (not is_valid(i, j) or solution[i][j] != 0 or seen[i][j]):
		return 0

	seen[i][j] = True
	result = 1
	directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
	for (di, dj) in directions:
		result += dfs(i + di, j + dj, seen)

	return result

def get_product_of_areas_of_connected_empty_squares():
	product = 1
	seen = [[False for j in range(n)] for i in range(n)]
	for i in range(n):
		for j in range(n):
			area = dfs(i, j, seen)
			if area > 0:
				product *= area
	return product

def main():
	backtrack()
	print_solution()
	answer = get_product_of_areas_of_connected_empty_squares()
	print(f"answer: {answer}")

main()
