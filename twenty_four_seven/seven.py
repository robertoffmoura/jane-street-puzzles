outside_top = ["--"] * 12
outside_left = ["--"] * 12
outside_right = ["--"] * 12
outside_bottom = ["--"] * 12
board = [["__" for j in range(12)] for i in range(12)]

square_top_left = [0 for i in range(7+1)]
square_top_right = [0 for i in range(7+1)]
square_bottom_left = [0 for i in range(7+1)]
square_bottom_right = [0 for i in range(7+1)]

left_row_sum = [0 for i in range(12)]
right_row_sum = [0 for i in range(12)]
top_column_sum = [0 for i in range(12)]
bottom_column_sum = [0 for i in range(12)]

left_row_count = [0 for i in range(12)]
right_row_count = [0 for i in range(12)]
top_column_count = [0 for i in range(12)]
bottom_column_count = [0 for i in range(12)]

top_most_stack = [[12] for i in range(12)]
left_most_stack = [[12] for i in range(12)]

def read_board():
	line = [s for s in input().split(" ") if s != ""]
	for j, s in enumerate(line):
		outside_top[j] = int(s) if s != "--" else "--"
	
	for i in range(12):
		line = [s for s in input().split(" ") if s != ""]
		outside_left[i] = int(line[0]) if line[0] != "--" else "--"
		outside_right[i] = int(line[-1]) if line[-1] != "--" else "--"
		for j, s in enumerate(line[1:-1]):
			if s == "__":
				continue
			n = int(s)
			board[i][j] = n
			if n == -1:
				continue
			if i < 7 and j < 7:
				square_top_left[n] += 1
			if i < 7 and j > 4:
				square_top_right[n] += 1
			if i > 4 and j < 7:
				square_bottom_left[n] += 1
			if i > 4 and j > 4:
				square_bottom_right[n] += 1
			if i < 7:
				top_column_sum[j] += n
				top_column_count[j] += 1
			if i > 4:
				bottom_column_sum[j] += n
				bottom_column_count[j] += 1
			if j < 7:
				left_row_sum[i] += n
				left_row_count[i] += 1
			if j > 4:
				right_row_sum[i] += n
				right_row_count[i] += 1
			if i < top_most_stack[j][0]:
				top_most_stack[j][0] = i
			if j < left_most_stack[i][0]:
				left_most_stack[i][0] = j
	
	line = [s for s in input().split(" ") if s != ""]
	for j, s in enumerate(line):
		outside_bottom[j] = int(s) if s != "--" else "--"


def print_board():
	print("   " + " ".join([f"{x:>2}" if x is not "--" else "--" for x in outside_top]))
	for i in range(12):
		print(f"{outside_left[i]:>2} " + " ".join([f"{x:>2}" if x not in ["--", -1] else "--" for x in board[i]]) + f" {outside_right[i]:>2}")
	print("   " + " ".join([f"{x:>2}" if x is not "--" else "--" for x in outside_bottom]))

def is_number(s):
	return s != "__" and s != -1

def valid_static(i, j):
	n = board[i][j]
	if i > 0 and j > 0:
		if is_number(board[i-1][j-1]) and is_number(board[i-1][j]) and is_number(board[i][j-1]):
			return False
	if i > 0 and j < 11:
		if is_number(board[i-1][j+1]) and is_number(board[i-1][j]) and is_number(board[i][j+1]):
			return False
	if i < 11 and j > 0:
		if is_number(board[i+1][j-1]) and is_number(board[i+1][j]) and is_number(board[i][j-1]):
			return False
	if i < 11 and j < 11:
		if is_number(board[i+1][j+1]) and is_number(board[i+1][j]) and is_number(board[i][j+1]):
			return False
	if i == top_most_stack[j][-1] and outside_top[j] != "--" and outside_top[j] <= 7:
		if n != outside_top[j]:
			return False
	if j == left_most_stack[i][-1] and outside_left[i] != "--" and outside_left[i] <= 7:
		if n != outside_left[i]:
			return False
	return True

def valid(i, j, n):
	if i > 0 and j > 0:
		if is_number(board[i-1][j-1]) and is_number(board[i-1][j]) and is_number(board[i][j-1]):
			return False
	if i > 0 and j < 11:
		if is_number(board[i-1][j+1]) and is_number(board[i-1][j]) and is_number(board[i][j+1]):
			return False
	if i < 11 and j > 0:
		if is_number(board[i+1][j-1]) and is_number(board[i+1][j]) and is_number(board[i][j-1]):
			return False
	if i < 11 and j < 11:
		if is_number(board[i+1][j+1]) and is_number(board[i+1][j]) and is_number(board[i][j+1]):
			return False
	if i < top_most_stack[j][-1] and outside_top[j] != "--" and outside_top[j] <= 7:
		if n != outside_top[j]:
			return False
	if j < left_most_stack[i][-1] and outside_left[i] != "--" and outside_left[i] <= 7:
		if n != outside_left[i]:
			return False
	if i < 7:
		if top_column_sum[j] + n > 20:
			return False
		if top_column_count[j] == 3 and top_column_sum[j] + n != 20:
			return False
		if j < 7:
			if square_top_left[n] == n:
				return False
		if j > 4:
			if square_top_right[n] == n:
				return False
	if i > 4:
		if bottom_column_sum[j] + n > 20:
			return False
		if bottom_column_count[j] == 3 and bottom_column_sum[j] + n != 20:
			return False
		if j < 7:
			if square_bottom_left[n] == n:
				return False
		if j > 4:
			if square_bottom_right[n] == n:
				return False
	if j < 7:
		if left_row_sum[i] + n > 20:
			return False
		if left_row_count[i] == 3 and left_row_sum[i] + n != 20:
			return False
	if j > 4:
		if right_row_sum[i] + n > 20:
			return False
		if right_row_count[i] == 3 and right_row_sum[i] + n != 20:
			return False
	return True

def place(i, j, n):
	board[i][j] = n
	if i < top_most_stack[j][-1]:
		top_most_stack[j].append(i)
	if j < left_most_stack[i][-1]:
		left_most_stack[i].append(j)
	if i < 7:
		top_column_sum[j] += n
		top_column_count[j] += 1
		if j < 7:
			square_top_left[n] += 1
		if j > 4:
			square_top_right[n] += 1
	if i > 4:
		bottom_column_sum[j] += n
		bottom_column_count[j] += 1
		if j < 7:
			square_bottom_left[n] += 1
		if j > 4:
			square_bottom_right[n] += 1
	if j < 7:
		left_row_sum[i] += n
		left_row_count[i] += 1
	if j > 4:
		right_row_sum[i] += n
		right_row_count[i] += 1

def remove(i, j, n):
	board[i][j] = "__"
	if i == top_most_stack[j][-1]:
		top_most_stack[j].pop()
	if j == left_most_stack[i][-1]:
		left_most_stack[i].pop()
	if i < 7:
		top_column_sum[j] -= n
		top_column_count[j] -= 1
		if j < 7:
			square_top_left[n] -= 1
		if j > 4:
			square_top_right[n] -= 1
	if i > 4:
		bottom_column_sum[j] -= n
		bottom_column_count[j] -= 1
		if j < 7:
			square_bottom_left[n] -= 1
		if j > 4:
			square_bottom_right[n] -= 1
	if j < 7:
		left_row_sum[i] -= n
		left_row_count[i] -= 1
	if j > 4:
		right_row_sum[i] -= n
		right_row_count[i] -= 1

def left_most(i):
	for j in range(7):
		if board[i][j] == "__" or board[i][j] == -1:
			continue
		return board[i][j]

def right_most(i):
	for j in range(11, 4, -1):
		if board[i][j] == "__" or board[i][j] == -1:
			continue
		return board[i][j]

def top_most(j):
	for i in range(7):
		if board[i][j] == "__" or board[i][j] == -1:
			continue
		return board[i][j]

def bottom_most(j):
	for i in range(11, 4, -1):
		if board[i][j] == "__" or board[i][j] == -1:
			continue
		return board[i][j]

def or_zero(n):
	return n if (n != "__" and n != -1) else 0

def partial_solve(start_i, end_i, start_j, end_j):
	finished = [False]

	def is_board_invalid(i, j):
		if j == 7:
			if left_row_count[i] != 4:
				return True
			if outside_left[i] != "--":
				if outside_left[i] > 7:
					if 40 - outside_left[i] != or_zero(board[i][5]) + or_zero(board[i][6]):
						return True
				else:
					if left_most(i) != outside_left[i]:
						return True
		if i == 6 and j > 1:
			if top_column_count[j-1] != 4:
				return True
			if outside_top[j-1] != "--":
				if outside_top[j-1] > 7:
					if 40 - outside_top[j-1] != or_zero(board[5][j-1]) + or_zero(board[6][j-1]):
						return True
				else:
					if top_most(j-1) != outside_top[j-1]:
						return True
		if j == 12:
			if right_row_count[i] != 4:
				return True
			if outside_right[i] != "--":
				if right_most(i) != outside_right[i]:
					return True
		if i == 11 and j > 1:
			if bottom_column_count[j-1] != 4:
				return True
			if outside_bottom[j-1] != "--":
				if bottom_most(j-1) != outside_bottom[j-1]:
					return True
		return False
	
	def reached_end_of_board(i, j):
		return i == 12 and j == 7

	def recurse(i=start_i, j=start_j):
		if is_board_invalid(i, j):
			return
		if j == end_j:
			j = start_j
			i += 1
		if i == end_i:
			if reached_end_of_board(i, j):
				if is_board_connected():
					print("FINAL SOLUTION")
					print_board()
					print("")
					finished[0] = True
				else:
					print("unconnected solution")
					print("")
			else:
				print("PARTIAL SOLUTION")
				print_board()
				print("")
				finished[0] = True
			return
		if board[i][j] == "__":
			board[i][j] = -1
			recurse(i, j+1)
			board[i][j] = "__"
			for n in range(7+1):
				if valid(i, j, n):
					place(i, j, n)
					recurse(i, j+1)
					if finished[0]:
						return
					remove(i, j, n)
		elif board[i][j] == -1:
			recurse(i, j+1)
		else:
			if valid_static(i, j):
				recurse(i, j+1)
	recurse()

def count_non_zero():
	result = 0
	for i in range(12):
		for j in range(12):
			if is_number(board[i][j]):
				result += 1
	return result

def in_board(i, j):
	return 0 <= i and i < 12 and 0 <= j and j < 12

def get_first_non_zero_element_j():
	j = 0
	while not is_number(board[0][j]):
		j += 1
	return j

def is_board_connected():
	i = 0
	j = get_first_non_zero_element_j()
	visited = [[False for j in range(12)] for i in range(12)]

	def count_connected(i, j):
		visited[i][j] = True
		if not is_number(board[i][j]):
			return 0
		result = 1
		for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
			if not in_board(i+di, j+dj) or visited[i+di][j+dj]:
				continue
			result += count_connected(i+di, j+dj)
		return result

	return count_connected(i, j) == count_non_zero()

def product_of_areas():
	visited = [[False for j in range(12)] for i in range(12)]

	def count_connected(i, j):
		visited[i][j] = True
		if is_number(board[i][j]):
			return 0
		count = 1
		for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
			if not in_board(i+di, j+dj) or visited[i+di][j+dj]:
				continue
			count += count_connected(i+di, j+dj)
		return count
	
	result = []
	for i in range(12):
		for j in range(12):
			if visited[i][j] or is_number(board[i][j]):
				continue
			result.append(count_connected(i, j))

	product = 1
	for item in result:
		product *= item
	return result, product

def solve():
	read_board()
	partial_solve(0, 7, 0, 7)
	partial_solve(0, 7, 7, 12)
	partial_solve(7, 12, 0, 7)
	partial_solve(7, 12, 7, 12)
	print(f"product of orthogonally adjacent areas = {product_of_areas()}")

solve()
