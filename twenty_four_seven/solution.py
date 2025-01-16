n = 7

UNDEFINED = -1
EMPTY = 0
board = [[UNDEFINED for j in range(n)] for i in range(n)]
solution = [[UNDEFINED for j in range(n)] for i in range(n)]
hints = [
	[0, 4, 0, 0, 0, 0, 0],
	[0, 0, 6, 3, 0, 0, 6],
	[0, 0, 0, 0, 0, 5, 5],
	[0, 0, 0, 4, 0, 0, 0],
	[4, 7, 0, 0, 0, 0, 0],
	[2, 0, 0, 7, 4, 0, 0],
	[0, 0, 0, 0, 0, 1, 0]
]

value_count = [0 for val in range(n+1)]
row_count = [0 for i in range(n)]
row_sum = [0 for i in range(n)]
col_count = [0 for j in range(n)]
col_sum = [0 for j in range(n)]

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def add_to_board(i, j, value):
	board[i][j] = value
	if value != EMPTY:
		value_count[value] += 1
		row_count[i] += 1
		row_sum[i] += value
		col_count[j] += 1
		col_sum[j] += value

def remove_from_board(i, j):
	value = board[i][j]
	board[i][j] = UNDEFINED
	if value != EMPTY:
		value_count[value] -= 1
		row_count[i] -= 1
		row_sum[i] -= value
		col_count[j] -= 1
		col_sum[j] -= value

def is_filled(i, j):
	return board[i][j] not in [UNDEFINED, EMPTY]

def has_unfilled_square_in_two_by_two_regions(i, j):
	if not is_filled(i, j):
		return True

	if i > 0 and j > 0:
		if all(is_filled(i + di, j+ dj) for (di, dj) in [(-1,-1), (-1,0), (0,-1)]):
			return False

	if i < n - 1 and j > 0:
		if all(is_filled(i + di, j+ dj) for (di, dj) in [(+1,-1), (+1,0), (0,-1)]):
			return False

	if i > 0 and j < n - 1:
		if all(is_filled(i + di, j+ dj) for (di, dj) in [(-1,+1), (-1,0), (0,+1)]):
			return False

	if i < n - 1 and j < n - 1:
		if all(is_filled(i + di, j+ dj) for (di, dj) in [(+1,+1), (+1,0), (0,+1)]):
			return False

	return True

def is_valid_addition(i, j, value):
	if value_count[value] > value:
		return False
	if row_count[i] > 4:
		return False
	if row_sum[i] > 20:
		return False
	if row_count[i] == 4 and row_sum[i] != 20:
		return False
	if j == n - 1 and not (row_count[i] == 4 and row_sum[i] == 20):
		return False
	if col_count[j] > 4:
		return False
	if col_sum[j] > 20:
		return False
	if col_count[j] == 4 and col_sum[j] != 20:
		return False
	if i == n - 1 and not (col_count[j] == 4 and col_sum[j] == 20):
		return False
	if not has_unfilled_square_in_two_by_two_regions(i, j):
		return False
	if j == n - 1 and not is_board_connected():
		return False
	return True

def is_valid(i, j):
	return 0 <= i < n and 0 <= j < n

def is_board_connected():
	start = None
	for i in range(n):
		for j in range(n):
			if board[i][j] != EMPTY:
				start = (i, j)
				break
		if start is not None:
			break
	if start is None:
		return True # Empty board

	q = [start]
	seen = set(q)
	while len(q) > 0:
		new_q = []
		for i, j in q:
			for di, dj in directions:
				ni, nj = i + di, j + dj
				if not is_valid(ni, nj) or (ni, nj) in seen or board[i][j] == EMPTY:
					continue
				seen.add((ni, nj))
				new_q.append((ni, nj))
		q = new_q
	
	for i in range(n):
		for j in range(n):
			if is_filled(i, j) and (i, j) not in seen:
				return False
	return True


def add_hints():
	for i in range(n):
		for j in range(n):
			if hints[i][j] != EMPTY:
				add_to_board(i, j, hints[i][j])

def save_solution():
	for i in range(n):
		for j in range(n):
			solution[i][j] = board[i][j]

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
	
	if board[i][j] != UNDEFINED:
		backtrack(i, j+1)
		return
	
	if print_count[0] == 1e3:
		print_board()
		print_count[0] = 0
	print_count[0] += 1
	
	for value in range(n+1):
		add_to_board(i, j, value)
		if is_valid_addition(i, j, value):
			backtrack(i, j+1)
		remove_from_board(i, j)

def dfs(i, j, seen):
	if (not is_valid(i, j) or solution[i][j] != EMPTY or seen[i][j]):
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
	add_hints()
	backtrack()
	print_solution()
	print(f"solution_count: {solution_count[0]}")
	answer = get_product_of_areas_of_connected_empty_squares()
	print(f"answer: {answer}")

main()