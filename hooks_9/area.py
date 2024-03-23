#      5   1   6   1   8   1  22   7   8 
#  55  5   5               5   5         
#   1      9   9   9   9       9       8 
#   6          6       4   4   4   7   8 
#   1      9       4   3               8 
#  24      9   6       3   1   2         
#   3      9           3       2   7     
#   6      9   6   6   6   6       7   8 
#   7      7       7       7       7     
#   2  5   8       8   8   8             

m = [[5, 5, 0, 0, 0, 5, 5, 0, 0],
     [0, 9, 9, 9, 9, 0, 9, 0, 8],
     [0, 0, 6, 0, 4, 4, 4, 7, 8],
     [0, 9, 0, 4, 3, 0, 0, 0, 8],
     [0, 9, 6, 0, 3, 1, 2, 0, 0],
     [0, 9, 0, 0, 3, 0, 2, 7, 0],
     [0, 9, 6, 6, 6, 6, 0, 7, 8],
     [0, 7, 0, 7, 0, 7, 0, 7, 0],
     [5, 8, 0, 8, 8, 8, 0, 0, 0]]

seen = set()
def dfs(i, j):
	if i < 0 or j < 0 or i > n-1 or j >n-1:
		return 0
	if m[i][j] != 0:
		return 0
	if (i, j) in seen:
		return 0
	seen.add((i, j))
	return 1 + dfs(i+1,j) + dfs(i-1,j) + dfs(i,j-1) + dfs(i,j+1)

result = 1
n = len(m)
for i in range(n):
	for j in range(n):
		a = dfs(i, j)
		if a > 0:
			print(a)
			result *= a
print(result)

