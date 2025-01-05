from collections import defaultdict

n = 100

def delete_last_lines(n):
	# Move the cursor to the start of the last line to be deleted
	print('\x1b[{}F'.format(n), end='')
	# Clear each of the last n lines
	for _ in range(n):
		print('\x1b[2K', end='')
	# Move the cursor back to the beginning of the line
	print('\r', end='')


neighbors = defaultdict(set)
for i in range(1, n+1):
	for j in range(1, n+1):
		if i == j or i%j != 0:
			continue
		neighbors[i].add(j)
		neighbors[j].add(i)

def solve():
	print_count = 0
	seen = set()
	best = []
	current = []
	def recurse(i):
		nonlocal print_count
		nonlocal best
		if i in seen:
			return
		seen.add(i)
		current.append(i)

		if print_count == 100000:
			delete_last_lines(2)
			print(" ".join([str(x) for x in current]))
			print(" ".join([str(x) for x in best]))
			print_count = 0
		print_count += 1

		if len(current) > len(best):
			best = current[:]
		for j in neighbors[i]:
			recurse(j)

		current.pop()
		seen.remove(i)

	for i in range(1, n+1):
		recurse(i)

	return best

print("\n\n", end="")
print(solve())