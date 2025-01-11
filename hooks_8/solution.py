from collections import deque

debug = False

if not debug:
	n = 9
	region_str = "\n".join([
	"🟨🟦🟦🟦🟨🟪🟪🟨🟨",
	"🟨🟦🟩🟩🟨🟦🟪🟨🟩",
	"🟨🟪🟪🟩🟩🟦🟦🟩🟩",
	"🟨🟪🟦🟦🟩🟦🟨🟪🟪",
	"🟨🟦🟦🟪🟪🟪🟨🟩🟩",
	"🟨🟪🟦🟦🟦🟪🟨🟨🟩",
	"🟨🟪🟪🟩🟨🟪🟦🟦🟨",
	"🟨🟨🟩🟩🟨🟪🟦🟦🟨",
	"🟨🟩🟩🟨🟨🟪🟪🟨🟨"])
else:
	n = 5
	region_str = "\n".join([
	"🟦🟦🟦🟪🟪",
	"🟨🟨🟦🟪🟩",
	"🟨🟩🟩🟩🟩",
	"🟨🟪🟪🟪🟩",
	"🟨🟪🟩🟩🟩"])

print(region_str)
hint = [[] for i in range(n+1)]
board = [[0 for j in range(n)] for i in range(n)]
solution = [[0 for j in range(n)] for i in range(n)]

region = [list(line) for line in region_str.split("\n") if line != ""]

pos_id = [[-1 for j in range(n)] for i in range(n)]
directions = [(0,1), (1,0), (0,-1), (-1,0)]

def get_neighbors(i, j):
	return [(i+di, j+dj) for (di, dj) in directions]

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

target_sum = sum(i**2 for i in range(n+1)) // region_count
region_sum = [0 for i in range(region_count)]
target_size = [0 for i in range(region_count)]
region_size = [0 for i in range(region_count)]
for i in range(n):
	for j in range(n):
		target_size[pos_id[i][j]] += 1

def add_to_board(i, j, value):
	board[i][j] = value
	region_id = pos_id[i][j]
	region_size[region_id] += 1
	region_sum[region_id] += value if value != -1 else 0

def remove_from_board(i, j):
	value = board[i][j]
	board[i][j] = 0
	region_id = pos_id[i][j]
	region_size[region_id] -= 1
	region_sum[region_id] -= value if value != -1 else 0

def has_unfilled_square_in_two_by_two_region(i, j):
	if board[i][j] <= 0:
		return True

	if i > 0 and j > 0:
		if board[i][j-1] > 0 and board[i-1][j] > 0 and board[i-1][j-1] > 0:
			return False

	if i > 0 and j < n-1:
		if board[i][j+1] > 0 and board[i-1][j] > 0 and board[i-1][j+1] > 0:
			return False

	if i < n-1 and j > 0:
		if board[i][j-1] > 0 and board[i+1][j] > 0 and board[i+1][j-1] > 0:
			return False

	if i < n-1 and j < n-1:
		if board[i][j+1] > 0 and board[i+1][j] > 0 and board[i+1][j+1] > 0:
			return False

	return True

def is_valid_addition(i, j):
	if not has_unfilled_square_in_two_by_two_region(i, j):
		return False
	region_id = pos_id[i][j]
	if region_size[region_id] < target_size[region_id]:
		return region_sum[region_id] <= target_sum
	else:
		return region_sum[region_id] == target_sum

if not debug:
	hint[8].append((0,2))
	add_to_board(0, 2, 8)
else:
	hint[4].append((0,1))
	hint[3].append((0,4))
	hint[5].append((4,0))
	hint[5].append((4,3))
	add_to_board(0, 1, 4)
	add_to_board(0, 4, 3)
	add_to_board(4, 0, 5)
	add_to_board(4, 3, 5)

def is_board_connected():
	start = (-1, -1)
	for i in range(n):
		for j in range(n):
			if board[i][j] > 0:
				start = (i, j)
				break
		if start[0] != -1:
			break

	if start[0] == -1:
		return True # Empty board.

	q = deque()
	q.append(start)
	seen = [[False for j in range(n)] for i in range(n)]
	seen[start[0]][start[1]] = True
	directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
	while len(q) > 0:
		i, j = q.popleft()
		for (di, dj) in directions:
			ni, nj = i + di, j + dj
			if not is_valid(ni, nj) or seen[ni][nj] or board[ni][nj] == -1:
				continue
			seen[ni][nj] = True
			q.append((ni, nj))

	for i in range(n):
		for j in range(n):
			if board[i][j] > 0 and not seen[i][j]:
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

def is_hook_valid(hook, hook_number):
	for (i, j) in hint[hook_number]:
		if (i, j) not in hook:
			return False

	for other_hook_number in range(1,n+1):
		if other_hook_number == hook_number:
			continue
		for (i, j) in hint[other_hook_number]:
			if (i, j) in hook:
				return False

	return True

def backtrack(sub_region = (0, n - 1, 0, n - 1),
			hook = [],
			idx = 0,
			hook_number = -1,
			seen_hook_numbers = set(),
			remaining_count = 0):

	if remaining_count < 0:
		return

	if len(hook) - idx < remaining_count:
		return

	if idx < len(hook):
		i, j = hook[idx]
		if board[i][j] != 0:
			backtrack(sub_region, hook, idx+1, hook_number, seen_hook_numbers, remaining_count)
			return

		add_to_board(i, j, hook_number)
		if is_valid_addition(i, j):
			backtrack(sub_region, hook, idx+1, hook_number, seen_hook_numbers, remaining_count-1)
		remove_from_board(i, j)

		add_to_board(i, j, -1)
		if is_valid_addition(i, j):
			backtrack(sub_region, hook, idx+1, hook_number, seen_hook_numbers, remaining_count)
		remove_from_board(i, j)
	else:
		if remaining_count != 0:
			return

		if not is_board_connected():
			return

		if len(seen_hook_numbers) == n:
			save_solution()
			print_solution()
			solution_count[0] += 1
			print("SOLUTION!!!")
			print("\n\n")
			return

		print_count[0] += 1
		if print_count[0] == 1e2:
			print_board()
			print_count[0] = 0

		for new_hook_number in reversed(range(1, n+1)):
			if new_hook_number in seen_hook_numbers:
				continue
			seen_hook_numbers.add(new_hook_number)

			new_hook_count = new_hook_number - len(hint[new_hook_number])
			top, bottom, left, right = sub_region
			top_row = [(top, j) for j in range(left, right+1)]
			bottom_row = [(bottom, j) for j in range(left, right+1)]
			left_col = [(i, left) for i in range(top, bottom+1)]
			right_col = [(i, right) for i in range(top, bottom+1)]
			if new_hook_number > 1:
				new_sub_region = (top+1, bottom, left+1, right)
				new_hook = sorted(list(set(top_row + left_col)))
				if is_hook_valid(new_hook, new_hook_number):
					backtrack(new_sub_region, new_hook, 0, new_hook_number, seen_hook_numbers, new_hook_count)

				new_sub_region = (top, bottom-1, left+1, right)
				new_hook = sorted(list(set(bottom_row + left_col)))
				if is_hook_valid(new_hook, new_hook_number):
					backtrack(new_sub_region, new_hook, 0, new_hook_number, seen_hook_numbers, new_hook_count)

				new_sub_region = (top+1, bottom, left, right-1)
				new_hook = sorted(list(set(top_row + right_col)))
				if is_hook_valid(new_hook, new_hook_number):
					backtrack(new_sub_region, new_hook, 0, new_hook_number, seen_hook_numbers, new_hook_count)

				new_sub_region = (top, bottom-1, left, right-1)
				new_hook = sorted(list(set(bottom_row + right_col)))
				if is_hook_valid(new_hook, new_hook_number):
					backtrack(new_sub_region, new_hook, 0, new_hook_number, seen_hook_numbers, new_hook_count)
			else:
				new_sub_region = (top+1, bottom, left+1, right)
				new_hook = sorted(list(set(top_row + left_col)))
				if is_hook_valid(new_hook, new_hook_number):
					backtrack(new_sub_region, new_hook, 0, new_hook_number, seen_hook_numbers, new_hook_count)
			
			seen_hook_numbers.remove(new_hook_number)

def dfs(i, j, seen):
	if (not is_valid(i, j) or solution[i][j] != -1 or seen[i][j]):
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
	print(f"solution_count: {solution_count[0]}")
	answer = get_product_of_areas_of_connected_empty_squares()
	print(f"answer: {answer}")

main()
