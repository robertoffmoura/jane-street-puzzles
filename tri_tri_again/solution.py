grid = [
	[  1,  71, 711, 711,   1,  17, 711,   1],
	[ 71,   1, 711,  17,  71,  71,  71, 711],
	[711,  71,  17,  71,  17, 711, 711,  71],
	[ 71,  17, 711,   1,  17, 711,  17,   1],
	[711, 711,   1,  17,   1,  17,   1, 711],
	[ 17,   1,  71, 711, 711, 711,  71,  17],
	[ 71,  71, 711,  71, 711,  17, 711,   1],
	[  1,   1,  17,  71,  17,   1,  71,  71],
	[ 71,  71,   1,  17,   1,  17, 711,  17],
	[  1, 711,  17, 711,  71,  71,  71,  71],
	[711,  71,   1,   1,  71,  71, 711,   1],
	[ 71,   1,  17, 711, 711,   1,  17,  71],
	[  1,  17,   1,  17,   1,  17, 711,  17],
	[ 71, 711,  17, 711,  71, 711,   1, 711],
	[711,  17,  71,   1,  17,  71,  17,   1],
	[  1,   1, 711, 711,  71, 711, 711,  17]
]
m, n = len(grid), len(grid[0])

def is_valid(i, j):
	return 0 <= i < m and 0 <= j < n

def generate_tetrahedron(current = []):
	if len(current) == 4:
		# print_tetrahedron(current)
		for j in range(n):
			backtrack(current, True, 0, j, 0, set())
		return
	for side in [1, 17, 71, 711]:
		if side in current:
			continue
		current.append(side)
		generate_tetrahedron(current)
		current.pop()

best = [float("inf")]

def backtrack(tetrahedron, upside_down = True, i = 0, j = 0, current_sum = 0, seen = set()):
	if not is_valid(i, j):
		return
	if tetrahedron[2] != grid[i][j]:
		return
	current_sum += grid[i][j]
	if i == m - 1:
		best[0] = min(best[0], current_sum)
		return
	if (i, j) in seen:
		return
	seen.add((i, j))
	if upside_down:
		backtrack(move_down_left(tetrahedron), False, i+1, j, current_sum, seen)
		backtrack(move_down_right(tetrahedron), False, i+1, j+1, current_sum, seen)
		backtrack(move_up(tetrahedron), False, i-1, j, current_sum, seen)
	else:
		backtrack(move_down(tetrahedron), True, i+1, j, current_sum, seen)
		backtrack(move_up_right(tetrahedron), True, i-1, j, current_sum, seen)
		backtrack(move_up_left(tetrahedron), True, i-1, j-1, current_sum, seen)
	seen.remove((i, j))

def move_down_left(t):
	return [t[3], t[2], t[0], t[1]]

def move_down_right(t):
	return [t[2], t[3], t[1], t[0]]

def move_up(t):
	return [t[0], t[1], t[3], t[2]]

def move_down(t):
	return [t[0], t[1], t[3], t[2]]

def move_up_left(t):
	return [t[3], t[2], t[0], t[1]]

def move_up_right(t):
	return [t[2], t[3], t[1], t[0]]


def print_tetrahedron(t, is_upside_down = False):
	if not is_upside_down:
		print(f"{t[0]:3}     {t[1]:3}")
		print(f"    {t[2]:3}    ")
		print(f"    {t[3]:3}    ")
		print("")
	else:
		print(f"    {t[3]:3}    ")
		print(f"    {t[2]:3}    ")
		print(f"{t[0]:3}     {t[1]:3}")
		print("")

generate_tetrahedron()
print(best[0])