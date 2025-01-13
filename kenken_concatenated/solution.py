from collections import namedtuple

n = 9
region_str = """
🟨🟨🟩🟩🟩🟪🟪🟨🟨
🟨🟦🟦🟦🟩🟪🟦🟦🟨
🟪🟪🟦🟦🟦🟨🟩🟦🟦
🟪🟨🟨🟩🟨🟨🟩🟨🟨
🟨🟨🟩🟩🟪🟪🟪🟨🟦
🟦🟦🟦🟩🟨🟨🟪🟦🟦
🟦🟦🟦🟨🟨🟪🟪🟩🟦
🟩🟪🟪🟪🟦🟦🟨🟩🟩
🟩🟩🟪🟦🟦🟦🟨🟨🟨
"""

print(region_str)
board = [[0 for j in range(n)] for i in range(n)]
solution = [[0 for j in range(n)] for i in range(n)]

region = [list(line) for line in region_str.split("\n") if line != ""]

point_to_region_id = [[-1 for j in range(n)] for i in range(n)]
directions = [(0,1), (1,0), (0,-1), (-1,0)]

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

def format_pos_id_row(row):
	return " ".join(f"{e:2}" for e in row)

print("region ids:")
print("\n".join([format_pos_id_row(row) for row in point_to_region_id]))
print("\n")

def get_region_id_to_points():
	region_id_to_points = [[] for k in range(region_count)]
	for i in range(n):
		for j in range(n):
			region_id = point_to_region_id[i][j]
			region_id_to_points[region_id].append((i,j))
	return region_id_to_points

region_id_to_points = get_region_id_to_points()

def get_end_of_region_points():
	return [points[-1] for points in region_id_to_points]

end_of_region_points = get_end_of_region_points()

Constraint = namedtuple("Constraint", "operation result")

region_to_constraint = {
	0: Constraint("/", 21),
	1: Constraint("*", 1960),
	2: Constraint("/", 13),
	3: Constraint("-", 17),
	4: Constraint("/", 5),
	5: Constraint("*", 969),
	6: Constraint("/", 21),
	7: Constraint("-", 66),
	8: Constraint("-", 1),
	9: Constraint("+", 63),
	10: Constraint("*", 342),
	11: Constraint("/", 9),
	12: Constraint("*", 59049),
	13: Constraint("+", 57),
	14: Constraint("-", 73),
	15: Constraint("-", 1),
	16: Constraint("-", 22),
	17: Constraint("+", 66),
	18: Constraint("/", 17),
	19: Constraint("+", 1009),
	20: Constraint("*", 1056),
}

row_count = [[0 for k in range(n+1)] for i in range(n)]
col_count = [[0 for k in range(n+1)] for j in range(n)]

def add_to_board(i, j, value):
	board[i][j] = value
	row_count[i][value] += 1
	col_count[j][value] += 1

def remove_from_board(i, j):
	value = board[i][j]
	board[i][j] = 0
	row_count[i][value] -= 1
	col_count[j][value] -= 1

def concatenate_values_in_same_row(points):
	i_values = sorted(set(i for (i,j) in points))
	result = []
	for i_val in i_values:
		current = 0
		for (i, j) in points:
			if i != i_val:
				continue
			current = 10 * current + board[i][j]
		result.append(current)
	return result

def evaluates_to_result(values, operation, expected):
	if operation == "*":
		result = 1
		for val in values:
			result *= val
		return result == expected
	if operation == "+":
		return sum(values) == expected
	if operation == "/":
		return values[0] == expected * values[1]
	if operation == "-":
		return abs(values[0] - values[1]) == expected

def get_values_in_region(region_id):
	points = region_id_to_points[region_id]
	return concatenate_values_in_same_row(points)

def satisfies_region_constraint(region_id):
	values = get_values_in_region(region_id)
	constraint = region_to_constraint[region_id]
	return evaluates_to_result(values, constraint.operation, constraint.result)

def is_valid_addition(i, j, value):
	if row_count[i][value] > 1:
		return False
	if col_count[j][value] > 1:
		return False
	if (i,j) in end_of_region_points:
		region_id = point_to_region_id[i][j]
		if not satisfies_region_constraint(region_id):
			return False
	return True

def save_solution():
	for i in range(n):
		for j in range(n):
			solution[i][j] = board[i][j]

def load_solution():
	for i in range(n):
		for j in range(n):
			board[i][j] = solution[i][j]

def print_grid(grid):
	for i in range(n):
		print(" ".join(f"{grid[i][j]:2}" if grid[i][j] > 0 else "  " for j in range(n)))

def print_solution():
	print_grid(solution)

def print_board():
	print_grid(board)
	print(f"\033[{n+1}A")

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
		print("\n\n")
		return

	if print_count[0] == 1e3:
		print_board()
		print_count[0] = 0
	print_count[0] += 1

	for digit in range(1,n+1):
		add_to_board(i, j, digit)
		if is_valid_addition(i, j, digit):
			backtrack(i, j+1)
		remove_from_board(i, j)

def get_sum_of_largest_number_of_each_region():
	return sum(max(get_values_in_region(region_id)) for region_id in range(region_count))

def main():
	backtrack()
	load_solution()
	print_solution()
	print(f"solution_count: {solution_count[0]}")
	answer = get_sum_of_largest_number_of_each_region()
	print(f"answer: {answer}")

main()
