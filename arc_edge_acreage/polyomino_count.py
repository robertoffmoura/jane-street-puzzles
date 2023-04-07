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

print(redelmeier(int(input())))