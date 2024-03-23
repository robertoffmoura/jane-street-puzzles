row_sum = [14, 24, 24, 39, 43, None, 22, 23, 29, 28, 34, 36, 29, 26, 26, 24, 20]
col_sum = [13, 20, 22, 28, 30, 36, 35, 39, 49, 39, 39, None, 23, 32, 23, 17, 13]
colors = ["🟩", "🟥", "🟨", "⬜", "⬛", "🟦", "🟧", "🟪", "🟫"]
n = 17
regions = [
	[(i, 0) for i in range(16)] + [(0, 1), (1, 1), (1, 2)] + [(15, 1), (15, 4)] + [(16, i) for i in range(6)] + [(14, 4), (14, 5)],
	[(i, 1) for i in range(2, 15)] + [(2, 2), (2, 3), (3, 2)] + [(14, 2), (15, 2), (15, 3)],
	[(i, j) for j in range(4, 7) for i in range(1, 4)] + [(0, 2), (0, 3), (1, 3)] + [(3, 3), (4, 3)],
	[(4+i, 2+i) for i in range(3)] + [(5+i, 2+i) for i in range(3)] + [(5, 5), (6, 5)],
	[(9+i, 2+j) for j in range(4) for i in range(-3+j, 3-j+1)],
	[(0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 9), (1, 8), (1, 7), (2, 7), (2, 9), (3, 9)],
	[(2, 10), (1, 10), (0, 10), (3, 10), (3, 11), (3, 12), (2, 12), (2, 13), (4, 12), (5, 12), (6, 12), (6, 11), (7, 11), (5, 11), (4, 11), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (1, 16), (1, 15), (2, 16), (3, 16), (4, 16)],
	[(2, 11), (1, 11), (1, 12), (1, 13), (1, 14), (2, 14), (3, 14), (3, 13), (4, 13), (5, 13), (5, 14), (6, 14)],
	[(2, 15), (3, 15), (4, 15), (4, 14), (5, 15), (5, 16), (6, 16), (6, 15), (7, 15), (7, 14), (7, 16), (8, 16), (8, 15), (9, 15), (9, 16), (9, 14), (10, 16), (11, 16), (12, 16), (12, 15), (12, 14), (11, 14), (13, 15), (13, 16), (14, 16), (15, 16), (16, 16), (16, 15), (15, 15), (15, 14), (16, 14)],
	[(2, 8), (3, 8), (3, 7), (4, 7), (4, 6), (4, 5), (4, 4), (5, 4)],
	[(5, 6), (5, 7), (5, 8), (4, 8), (6, 8), (6, 7), (6, 6), (7, 6), (7, 5), (8, 5), (8, 6)],
	[(5, 9), (6, 9), (7, 9), (7, 8), (7, 7), (8, 7), (9, 7), (9, 6), (10, 6), (10, 5), (11, 5), (11, 4)],
	[(4, 9), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (8, 8), (8, 9), (8, 11), (8, 12), (7, 12), (9, 12)],
	[(6, 13), (7, 13), (8, 13), (8, 14), (9, 13), (9, 11), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15), (11, 15)],
	[(14, 3), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (11, 6), (11, 7), (11, 8), (10, 7), (10, 8)],
	[(9, 8), (9, 9), (10, 9), (10, 10), (11, 10), (11, 11), (12, 11), (12, 12)],
	[(11, 12), (11, 13), (12, 13), (13, 11), (13, 12), (13, 13), (13, 14), (14, 10), (14, 11), (14, 14), (14, 15)],
	[(11, 9), (12, 8), (12, 9), (12, 10), (13, 8), (13, 10), (14, 7), (14, 8)],
	[(13, 9), (14, 9), (14, 12), (14, 13), (15, 7), (15, 8), (15, 9), (15, 10), (15, 11), (15, 12), (15, 13), (16, 13)],
	[(14, 6), (15, 5), (15, 6), (16, 6), (16, 7), (16, 8), (16, 9), (16, 10), (16, 11), (16, 12)]
]
index_to_region = {}
for r in range(len(regions)):
	for i, j in regions[r]:
		index_to_region[(i, j)] = r
board = [[0 for j in range(n)] for i in range(n)]
grid = [["  " for i in range(n + n + 1)] for i in range(n + n + 1)]

def make_empty_grid():
	return [["  " for i in range(n + n + 1)] for i in range(n + n + 1)]

def print_regions():
	grid = [["-1" for j in range(n)] for i in range(n)]
	for r in range(len(regions)):
		for i,j in regions[r]:
			grid[i][j] = colors[r%(len(colors))]
	for i in range(n):
		print("".join(grid[i]))

def is_a_border(i1, j1, i2, j2):
	return index_to_region[(i1, j1)] != index_to_region[(i2, j2)]

def write_board_to_grid():
	for i in range(n):
		for j in range(n):
			e = board[i][j]
			grid[1+2*i][1+2*j] = f"{e:>2}"

def write_borders_to_grid():
	for i in range(n):
		for j in range(n-1):
			if is_a_border(i, j, i, j+1):
				grid[2+2*i][2+2*j] = "⬜"
				grid[1+2*i][2+2*j] = "⬜"
				grid[2*i][2+2*j] = "⬜"
	for j in range(n):
		for i in range(n-1):
			if is_a_border(i, j, i+1, j):
				grid[2+2*i][2+2*j] = "⬜"
				grid[2+2*i][1+2*j] = "⬜"
				grid[2+2*i][2*j] = "⬜"
	for i in range(n + n + 1):
		grid[i][0] = "⬜"
		grid[i][-1] = "⬜"
	for j in range(n + n + 1):
		grid[0][j] = "⬜"
		grid[-1][j] = "⬜"

def print_grid():
	for i in range(n + n + 1):
		s = f"{row_sum[i//2]:>2}" if i%2 == 1 and row_sum[i//2] != None else "  "
		print(s, end=" ")
		print("".join(grid[i]))
	print("", end="   ")
	for j in range(n + n + 1):
		s = f"{col_sum[j//2]:>2}" if j%2 == 1 and col_sum[j//2] != None else "  "
		print(s, end="")
	print("")


def write_current_to_grid():
	mat = [[None for j in range(3*scale)] for i in range(3*scale)]

	for i in range(scale):
		for j in range(2*scale):
			mat[i][j] = scale
	for i in range(scale, 2*scale):
		for j in range(scale, 3*scale):
			mat[i][j] = scale
	for i in range(2*scale, 3*scale):
		for j in range(scale, 2*scale):
			mat[i][j] = scale
	
	m = 3*scale
	# Flip horizontally
	if rotation//4 > 0:
		for i in range(m):
			for j in range(m//2):
				mat[i][j], mat[i][m - 1 - j] = mat[i][m - 1 - j], mat[i][j]
	
	# Rotate a multiple of 90 degrees 
	for k in range(rotation%4):
		for i in range((m+1)//2):
			for j in range(m//2):
				mat[i][j], mat[j][m-1-i], mat[m-1-i][m-1-j], mat[m-1-j][i] = mat[j][m-1-i], mat[m-1-i][m-1-j], mat[m-1-j][i], mat[i][j]

	for i in range(m):
		for j in range(m):
			if mat[i][j] is None:
				continue
			i2, j2 = current_i + i, current_j + j
			if board[i2][j2] == 0:
				grid[1+2*i2][1+2*j2] = f"{mat[i][j]:>2}"
			else:
				grid[1+2*i2][1+2*j2] = "❌"
	
	print(f"rotation = {rotation}")
	for i in range(m):
		print(" ".join([str(x) if x is not None else " " for x in mat[i]]))

			

print_regions()

current_i, current_j = (0, 0)
scale = 1
rotation = 0

while True:
	grid = make_empty_grid()
	write_board_to_grid()
	write_borders_to_grid()
	write_current_to_grid()
	print_grid()
	key = input()
	if key == "w":
		current_i -= 1
	elif key == "s":
		current_i += 1
	elif key == "a":
		current_j -= 1
	elif key == "d":
		current_j += 1
	elif key == "+":
		scale += 1
	elif key == "-":
		scale -= 1
	elif key == "r":
		rotation += 1
		rotation %= 8