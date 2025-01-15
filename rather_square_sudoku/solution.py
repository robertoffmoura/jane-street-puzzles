n = 9

UNDEFINED = 0
board = [[UNDEFINED for j in range(n)] for i in range(n)]
solution = [[UNDEFINED for j in range(n)] for i in range(n)]
row_count = [[0 for k in range(n+1)] for i in range(n)]
col_count = [[0 for k in range(n+1)] for j in range(n)]
square_count = [[[0 for k in range(n+1)] for j in range(n//3)] for i in range(n//3)]

product_constraint = [
	[ 0,  0,  9,  0,  0,  9, 49,  0,  0],
	[ 9,  0, 25,  0,  0,  0, 36,  0,  0],
	[49,  0,  0, 36, 16,  9,  0, 81, 25],
	[ 4, 49,  0,  1,  0,  0,  9,  0, 81],
	[ 0,  0, 81,  0,  0,  0, 16,  0,  0],
	[ 9,  0, 64,  0,  0,  4,  0,  4,  6],
	[36, 16,  0, 16,  4, 25,  0,  0, 49],
	[ 0,  0, 49,  0,  0,  0,  9,  0,  4],
	[ 0,  0, 36, 49,  0,  0, 16,  0,  0]
]

directions = [(0,1), (1,0), (0,-1), (-1,0)]

def get_divisor_pairs():
	divisor_pairs = [[] for _ in range(n**2 + 1)]
	for a in range(1, n+1):
		for b in range(a, n+1):
			divisor_pairs[a*b].append((a, b))
	return divisor_pairs

divisor_pairs = get_divisor_pairs()

def get_divisors():
	divisors = [set() for _ in range(n**2 + 1)]
	for a in range(1, n+1):
		for b in range(a, n+1):
			divisors[a*b].add(a)
			divisors[a*b].add(b)
	return divisors

divisors = get_divisors()

def is_valid(i, j):
	return 0 <= i < n and 0 <= j < n

def add_to_board(i, j, value):
	board[i][j] = value
	row_count[i][value] += 1
	col_count[j][value] += 1
	square_count[i//3][j//3][value] += 1

def remove_from_board(i, j):
	value = board[i][j]
	board[i][j] = UNDEFINED
	row_count[i][value] -= 1
	col_count[j][value] -= 1
	square_count[i//3][j//3][value] -= 1

def satisfies_product_constraint(i, j):
	neighbors = [board[i + di][j + dj] for di, dj in directions if is_valid(i + di, j + dj)]
	if neighbors.count(UNDEFINED) >= 2:
		return True
	product = product_constraint[i][j]
	if neighbors.count(UNDEFINED) == 1:
		return any(value in divisors[product] for value in neighbors)
	else: # neighbors.count(UNDEFINED) == 0:
		for a, b in divisor_pairs[product]:
			if a == b:
				if neighbors.count(a) >= 2:
					return True
			else:
				if neighbors.count(a) >= 1 and neighbors.count(b) >= 1:
					return True
	return False

def is_valid_addition(i, j, value):
	if row_count[i][value] > 1 or col_count[j][value] > 1 or square_count[i//3][j//3][value] > 1:
		return False
	for di, dj in directions:
		ni, nj = i + di, j + dj
		if not is_valid(ni, nj):
			continue
		if product_constraint[ni][nj] != UNDEFINED:
			if not satisfies_product_constraint(ni, nj):
				return False
	return True

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

	if print_count[0] == 1e3:
		print_board()
		print_count[0] = 0
	print_count[0] += 1

	for value in range(1, n+1):
		add_to_board(i, j, value)
		if is_valid_addition(i, j, value):
			backtrack(i, j+1)
		remove_from_board(i, j)

def get_sum_of_squares_of_gray_numbers():
	result = 0
	for i in range(n):
		for j in range(n):
			if product_constraint[i][j] == UNDEFINED:
				continue
			result += solution[i][j]**2
	return result

def main():
	backtrack()
	print_solution()
	print(f"solution_count: {solution_count[0]}")
	answer = get_sum_of_squares_of_gray_numbers()
	print(f"answer: {answer}")

main()