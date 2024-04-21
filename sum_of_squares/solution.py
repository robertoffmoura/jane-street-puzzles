n = 5
board = [[None for j in range(n)] for i in range(n)]
found_solution = [False]

row_divisor = [None, 2, 3, 4, None]
col_divisor = [6, 7, 8, 9, 10]

def row_is_divisible(i):
	if i == 1:
		return board[1][4] % 2 == 0
	if i == 2:
		return sum(board[2]) % 3 == 0
	if i == 3:
		return (10*board[3][3] + board[3][4]) % 4 == 0
	# row = board[i]
	# return int("".join([str(e) for e in row])) % row_divisor[i] == 0

def col_is_divisible(j):
	if j == 0:
		return board[4][0] % 2 == 0 and sum(board[i][0] for i in range(n)) % 3 == 0
	if j == 1:
		return (10000*board[0][1] + 1000*board[1][1] + 100*board[2][1] + 10*board[3][1] + board[4][1]) % 7 == 0
	if j == 2:
		return (100*board[2][2] + 10*board[3][2] + board[4][2]) % 8 == 0
	if j == 3:
		return sum(board[i][3] for i in range(n)) % 9 == 0
	if j == 4:
		return board[4][4] == 0
	# col = [board[i][j] for i in range(n)]
	# return int("".join([str(e) for e in col])) % col_divisor[j] == 0

def print_board():
	print("\n".join([" ".join([str(board[i][j]) if board[i][j] is not None else "-" for j in range(n)]) for i in range(n)]))

def recurse(k, idx=0):
	if found_solution[0]:
		return
	if idx == n**2:
		if k > 0:
			return
		print("solution:")
		print_board()
		print(f"sum: {9*n**2 - remaining}")
		found_solution[0] = True
		return
	# i, j = idx//n, idx%n
	j, i = n-1-idx//n, n-1-idx%n
	for d in range(10):
		if k - d < 0:
			break 
		board[i][j] = 9 - d
		# if j == n-1 and row_divisor[i] is not None:
		if j == 0 and row_divisor[i] is not None:
			if not row_is_divisible(i):
				board[i][j] = None
				continue
		# if i == n-1 and col_divisor[j] is not None:
		if i == 0 and col_divisor[j] is not None:
			if not col_is_divisible(j):
				board[i][j] = None
				continue
		recurse(k - d, idx+1)
	board[i][j] = None

remaining = 0
while not found_solution[0]:
	recurse(remaining)
	remaining += 1
