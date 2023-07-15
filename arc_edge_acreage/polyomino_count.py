def redelmeier(n):
	count = [0]
	polyomino = []
	untried_set = [(0,0)]
	polyomino_neighbors = set()

	def get_neighbors(square):
		neighbors = []
		x, y = square
		for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
			if y + dy < 0 or (y + dy == 0 and x + dx < 0):
				continue
			new_square = (x + dx, y + dy)
			if new_square in polyomino_neighbors or new_square in polyomino:
				continue
			neighbors.append(new_square)
		return neighbors

	def redelmeier_recursion(untried_set):
		while len(untried_set) > 0:
			new_square = untried_set.pop()
			if len(polyomino) == n-1:
				count[0] += 1
				print_polyomino(polyomino + [new_square])
				continue
			new_neighbors = get_neighbors(new_square)
			new_untried_set = untried_set.copy()
			new_untried_set.extend(new_neighbors)
			for s in new_neighbors:
				polyomino_neighbors.add(s)
			polyomino.append(new_square)
			redelmeier_recursion(new_untried_set)
			polyomino.pop()
			for s in new_neighbors:
				polyomino_neighbors.remove(s)

	redelmeier_recursion(untried_set)
	return count[0]

def print_polyomino(l):
	min_x, min_y = float("inf"), float("inf")
	max_x, max_y = float("-inf"), float("-inf")
	for x, y in l:
		min_x = min(min_x, x)
		min_y = min(min_y, y)
		max_x = max(max_x, x)
		max_y = max(max_y, y)
	result = [["  " for x in range(min_x, max_x+1)] for y in range(min_y, max_y+1)]
	for x,y in l:
		result[max_y - (y - min_y)][x - min_x] = "🟩"
	print("\n".join(["".join(row) for row in result]))
	print("")

print(redelmeier(int(input())))