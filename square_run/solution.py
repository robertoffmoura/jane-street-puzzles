board = [
	[ 8,  5, 13, 23, 29, 15, 23, 30],
	[17, 22, 30,  3, 13, 25,  2, 14],
	[10, 15, 18, 28,  2, 18, 27,  6],
	[ 0, 31,  1, 11, 22,  7, 16, 20],
	[12, 17, 24, 26,  3, 24, 25,  5],
	[27, 31,  8, 11, 19,  4, 12, 21],
	[21, 20, 28,  4,  9, 26,  7, 14],
	[ 1,  6,  9, 19, 29, 10, 16,  0]
]

n = len(board)
start = (n-1,0)
end = (0,n-1)
squares = set(i**2 for i in range(10))
directions = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]

def point_to_string(i, j):
	return chr(ord("a") + j) + chr(ord("0") + n - i)

def journey_to_string(l):
	return ", ".join(point_to_string(*e) for e in l)

def sums_to_string(l):
	return " + ".join(str(e) for e in l)

def is_valid(i, j):
	return 0 <= i < n and 0 <= j < n

d = {}
def solve(i = n-1, j = 0, offset = 0):
	if (i, j, offset) in d:
		return d[(i, j, offset)]

	if i == 0 and j == n-1:
		return board[i][j], [(i, j)], [board[i][j]]

	best_score = 0
	best_journey = []
	best_sums = []

	for di, dj in directions:
		for distance in range(1, n):
			ni, nj = i + distance * di, j + distance * dj
			if not is_valid(ni, nj):
				continue
			if offset > 100:
				continue
			sums_to_perfect_square = (board[i][j] + board[ni][nj] - 2 * offset) in squares
			new_offset = offset + (1 if sums_to_perfect_square else 5)
			new_score, new_journey, new_sums = solve(ni, nj, new_offset)
			if new_score > best_score:
				best_score = new_score
				best_journey = new_journey
				best_sums = new_sums

	result_score = best_score + board[i][j] - offset
	result_journey = [(i, j)] + best_journey
	result_sums = [board[i][j] - offset] + best_sums
	result = result_score, result_journey, result_sums
	d[(i, j, offset)] = result
	return result

score, journey, sums = solve()
print("best:", score - 1)
print(journey_to_string(journey[1:]))
print(sums_to_string(sums[1:]))