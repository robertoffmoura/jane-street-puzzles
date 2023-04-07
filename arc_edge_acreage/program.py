def count_polyominos(n):
	neighbors = [(0,1), (1,0), (0,-1), (-1,0)]
	result = [0]
	current = []
	def recurse(stack=[(0,0)]):
		if len(current) == n:
			result[0] += 1
			print(current)
			print_polyomino(current)
			print("")
			return
		for i,(x,y) in enumerate(stack):
			stack_copy = stack[i+1:]
			for dx, dy in neighbors:
				if not(y+dy > 0 or (y+dy == 0 and x+dx >= 0)):
					continue
				if (x+dx, y+dy) in current:
					continue
				if (x+dx, y+dy) in stack:
					continue
				stack_copy.append((x+dx, y+dy))
			current.append((x, y))
			recurse(stack_copy)
			current.pop()
	recurse()
	print(result)

# def count_polyominos(n):
# 	steps = [(0,1), (1,0), (0,-1), (-1,0)]
# 	result = [0]
# 	current = [(0,0)]
# 	seen = set()

# 	def get_neighbors(x, y):
# 		result = []
# 		for dx, dy in steps:
# 			if not(y+dy > 0 or (y+dy == 0 and x+dx >= 0)):
# 				continue
# 			if (x+dx, y+dy) in current:
# 				continue
# 			if (x+dx, y+dy) in seen:
# 				continue
# 			result.append((x+dx, y+dy))
# 		return result

# 	def recurse(x=0, y=0):
# 		if len(current) == n:
# 			result[0] += 1
# 			print(current)
# 			print_polyomino(current)
# 			print("")
# 			return
# 		neighbors = get_neighbors(x, y)
# 		for x2, y2 in neighbors:
# 			current.append((x2, y2))
# 			recurse(x2, y2)
# 			current.pop()
# 			seen.add((x2, y2))
# 		for x2, y2 in neighbors:
# 			seen.remove((x2, y2))
# 	recurse()
# 	print(result)

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

count_polyominos(int(input()))

