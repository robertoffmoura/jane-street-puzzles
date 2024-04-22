grid = [
	[ 1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1, -1, -1, -1, -1, -1],
	[ 5,  5,  5,  5, -1, -1, -1, -1, -1],
	[-1, -1, -1, -1,  0, -1, -1, -1, -1],
	[-1, -1, -1, -1,  0, -1, -1,  8,  0],
	[-1, -1, -1, -1,  0, -1, -1, -1,  0],
	[-1, -1, -1, -1,  0, -1, -1,  9,  9]
]
n = 9
row_sum = [26, 42, 11, 22, 42, 36, 29, 32, 45]
col_sum = [31, 19, 45, 16, 5, 47, 28, 49, 45]

remaining = {d:d for d in range(1, n+1)}
for i in range(n):
	for j in range(n):
		if grid[i][j] in [0,-1]:
			continue
		remaining[grid[i][j]] -= 1

remaining_count = [len([1 for d in range(1, n+1) if remaining[d] > 0])]
found_solution = [False]

def go_up_n_lines(count):
	return f"\033[{count}A"

def print_board():
	print("--" * n)
	for i in range(n):
		print(" ".join([str(d) if d not in [0,-1] else " " for d in grid[i]]) + "|")
	print("--" * n)
	print("")

def row_sums_to_target(i):
	return sum(grid[i]) == row_sum[i]

def col_sums_to_target(j):
	return sum(grid[i][j] for i in range(n)) == col_sum[j]

def add_to_grid(i, j, d):
	remaining[d] -= 1
	if remaining[d] == 0:
		remaining_count[0] -= 1
	grid[i][j] = d

def remove_from_grid(i, j, d):
	grid[i][j] = -1
	if remaining[d] == 0:
		remaining_count[0] += 1
	remaining[d] += 1

print_count = [0]
def recurse(idx=1):
	print_count[0] += 1
	if print_count[0] == 100000:
		print_board()
		print("")
		print(go_up_n_lines(n+4), end="")
		print_count[0] = 0

	if found_solution[0]:
		return
	
	i, j = (idx-1)//n, (idx-1)%n
	if j == n-1 and not row_sums_to_target(i):
		return
	if i == n-1 and not col_sums_to_target(j):
		return

	i, j = idx//n, idx%n

	if idx == n**2 - 1:
		if remaining_count[0] != 0:
			return
		print_board()
		found_solution[0] = True

	if grid[i][j] != -1:
		recurse(idx+1)
		return
	
	d = max(i,j)+1
	grid[i][j] = 0
	recurse(idx+1)
	grid[i][j] = -1
	if remaining[d] > 0:
		add_to_grid(i, j, d)
		recurse(idx+1)
		remove_from_grid(i, j, d)

recurse()
