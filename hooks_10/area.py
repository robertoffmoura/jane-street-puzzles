# After running solution.py to get the intersection of partial solutions
# we can just compute the full solution manually from there.

board = [
	[9, 0, 9, 9, 0, 0, 0, 0, 0],
	[7, 0, 0, 7, 0, 0, 7, 7, 9],
	[6, 0, 0, 5, 5, 5, 8, 0, 9],
	[6, 3, 4, 4, 0, 5, 0, 7, 9],
	[0, 0, 2, 0, 4, 0, 8, 0, 0],
	[0, 0, 2, 1, 4, 5, 8, 7, 9],
	[0, 0, 3, 0, 0, 3, 0, 0, 9],
	[6, 6, 6, 6, 0, 0, 8, 7, 9],
	[0, 8, 0, 8, 8, 0, 8, 0, 0]
]

seen = set()
def dfs(i, j):
	if i < 0 or j < 0 or i > n-1 or j >n-1:
		return 0
	if board[i][j] != 0:
		return 0
	if (i, j) in seen:
		return 0
	seen.add((i, j))
	return 1 + dfs(i+1,j) + dfs(i-1,j) + dfs(i,j-1) + dfs(i,j+1)

result = 1
n = len(board)
for i in range(n):
	for j in range(n):
		a = dfs(i, j)
		if a > 0:
			print(a)
			result *= a
print("answer:")
print(result)