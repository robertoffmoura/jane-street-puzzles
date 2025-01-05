n = 11

board = [[-1 for j in range(n)] for i in range(n)]
default_regions = [
	[(0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)],
	[(1, 3), (1, 2), (1, 1), (2, 2), (2, 1), (3, 2), (3, 1), (4, 1)],
	[(0, 3), (0, 4), (0, 5), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (4, 2), (4, 3)],
	[(6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (7, 1), (8, 1), (10, 1), (10, 2), (9, 3), (10, 3), (9, 4), (10, 4), (9, 5)],
	[(5, 1), (6, 1), (5, 2), (6, 2), (5, 3), (6, 3), (7, 3), (4, 4), (5, 4), (6, 4), (4, 5), (5, 5), (5, 6), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (0, 8), (1, 8), (2, 8), (0, 9), (1, 9), (2, 9), (0, 10), (7, 8), (8, 8), (9, 8), (10, 8), (8, 9), (9, 9), (10, 9), (7, 10), (8, 10)],
	[(5, 8), (6, 8), (4, 9), (5, 9), (6, 9), (7, 9), (6, 10)],
	[(4, 8), (3, 8), (3, 9), (4, 10), (3, 10), (2, 10), (1, 10)],
	[(5, 10)],
	[(9, 1), (9, 2), (8, 2), (7, 2), (8, 4), (8, 3), (7, 4)],
	[(10, 10), (9, 10)],
	[(10, 7), (10, 6), (10, 5), (9, 6), (8, 6), (8, 5), (7, 6), (7, 5), (6, 6), (6, 5)],
	[(4, 6), (3, 6), (3, 5)],
	[(2, 6), (1, 6), (0, 6), (0, 7)],
]
default_point_to_region = [[None for j in range(n)] for i in range(n)]
for idx,region in enumerate(default_regions):
	for i,j in region:
		default_point_to_region[i][j] = idx
black_squares = set()
row_to_black_squares = [None for i in range(n)]
point_to_region_stack = [default_point_to_region]

def is_palindrome(x):
	return str(x) == str(x)[::-1]

fib = [1, 2]
while len(str(fib[-1])) <= 11:
	fib.append(fib[-1] + fib[-2])
fib = set(fib)

def is_fibonacci(x):
	return x in fib

def sum_of_digits(x):
	result = 0
	while x > 0:
		result += x % 10
		x //= 10
	return result

squares = set()
i = 1
while len(str(i**2)) <= 11:
	squares.add(i**2)
	i += 1

def is_square(x):
	return x in squares

is_prime = [True for i in range(10**6)]
is_prime[1] = False
for i in range(2, 10**3):
	for j in range(i**2, 10**6, i):
		is_prime[j] = False
primes = [i for i in range(2, 10**6) if is_prime[i]]

primes_to_prime_power = set()
for i in primes:
	for j in primes:
		if i**j > 10**n:
			break
		primes_to_prime_power.add(i**j)

def is_prime_raised_to_prime_power(x):
	return x in primes_to_prime_power

def product_of_digits(x):
	result = 1
	while x > 0:
		result *= x % 10
		x //= 10
	return result

def ends_in_1(x):
	return x % 10 == 1

conditions = [
	lambda x: is_square(x),
	lambda x: is_palindrome(x - 1),
	lambda x: is_prime_raised_to_prime_power(x),
	lambda x: sum_of_digits(x) == 7,
	lambda x: is_fibonacci(x),
	lambda x: is_square(x),
	lambda x: x % 37 == 0,
	lambda x: is_palindrome(x) and x % 23 == 0,
	lambda x: ends_in_1(product_of_digits(x)),
	lambda x: x % 88 == 0,
	lambda x: is_palindrome(x + 1)
]

def place_black_square(i, j):
	black_squares.add((i,j))

def remove_black_square(i, j):
	black_squares.remove((i,j))

def get_point_to_region_mapping():
	point_to_region = [[None for j in range(n)] for i in range(n)]
	region_count = 0
	old_point_to_region = point_to_region_stack[-1]

	def valid(i, j):
		return 0 <= i < n and 0 <= j < n

	def get_neighbors(i, j):
		return [(i+di,j+dj) for (di,dj) in [(0,1),(1,0),(0,-1),(-1,0)]]

	def recurse(i, j):
		if (i, j) in black_squares or point_to_region[i][j] is not None:
			return 0
		point_to_region[i][j] = region_count
		for i2, j2 in get_neighbors(i, j):
			if not valid(i2, j2) or old_point_to_region[i][j] != old_point_to_region[i2][j2]:
				continue
			recurse(i2, j2)
		return 1

	for i in range(n):
		for j in range(n):
			if recurse(i, j):
				region_count += 1
	return point_to_region

def get_region_to_number_mapping(point_to_region):
	region_to_number = {}
	for i in range(n):
		for j in range(n):
			d = board[i][j]
			if d == -1:
				continue
			region = point_to_region[i][j]
			if region in region_to_number and d != region_to_number[region]:
				print("Squares in the same region can't have different numbers")
			if region not in region_to_number:
				region_to_number[region] = d
	return region_to_number

def can_place_black_square(current, i, j):
	if j == 1 or j == n-2:
		return False
	left = current[-1] + 1 if len(current) > 0 else 0
	right = j
	if (i+1, j) in black_squares:
		return False
	if left == right:
		return True
	place_black_square(i, j)
	point_to_region = get_point_to_region_mapping()
	region_to_number = get_region_to_number_mapping(point_to_region)
	number_placements = get_number_placements(point_to_region[i][left:right], region_to_number.copy(), conditions[i])
	remove_black_square(i, j)
	return len(number_placements) > 0

def get_number_placements(point_to_region, region_to_number, condition):
	def current_to_number(current):
		return sum([current[~j] * 10**j for j in range(len(current))])
	result = []
	current = []
	def recurse(j=0):
		if j == len(point_to_region):
			if condition(current_to_number(current)):
				result.append(current[:])
			return
		region = point_to_region[j]
		if region in region_to_number:
			current.append(region_to_number[region])
			recurse(j+1)
			current.pop()
			return
		for d in range(10):
			if j == 0 and d == 0:
				continue
			if j > 0 and region != point_to_region[j-1] and d == region_to_number[point_to_region[j-1]]:
				continue
			region_to_number[region] = d
			current.append(d)
			recurse(j+1)
			current.pop()
			del region_to_number[region]
	recurse()
	return result

def get_black_square_placements_for_row(i):
	result = []
	current = []
	def recurse(j=0):
		if j >= n:
			if can_place_black_square(current, i, n):
				result.append(current[:])
			return
		recurse(j+1)
		if can_place_black_square(current, i, j):
			place_black_square(i, j)
			current.append(j)
			recurse(j+3)
			current.pop()
			remove_black_square(i, j)
	recurse()
	return result

def add_black_squares_to_row(black_square_placement, i):
	for j in black_square_placement:
		place_black_square(i, j)
	row_to_black_squares[i] = black_square_placement

def remove_black_squares_from_row(i):
	black_square_placement = row_to_black_squares[i]
	for j in black_square_placement:
		remove_black_square(i, j)
	row_to_black_squares[i] = None

def erase_lines(n):
	for _ in range(n):
		print("\033[A\033[K", end="")

def print_board():
	for i in range(n):
		print(" ".join([str(x) if x != -1 else " " for x in board[i]]))
	print("")

def get_intervals(black_square_placement):
	result = []
	start = 0
	for j in black_square_placement + [n]:
		end = j
		if end - start > 0:
			result.append((start, end))
		start = j+1
	return result

def get_number_placements_for_row(i):
	black_square_placement = row_to_black_squares[i]
	intervals = get_intervals(black_square_placement)
	point_to_region = point_to_region_stack[-1]
	result = []
	def recurse(k=0):
		if k == len(intervals):
			result.append(board[i][:])
			return
		left, right = intervals[k]
		region_to_number = get_region_to_number_mapping(point_to_region)
		number_placements = get_number_placements(point_to_region[i][left:right], region_to_number.copy(), conditions[i])
		for number_placement in number_placements:
			add_numbers_to_row(number_placement, i, left, right)
			recurse(k+1)
			remove_numbers_from_row(i, left, right)
	recurse()
	return result

def add_numbers_to_row(number_placement, i, j_start=0, j_end=n):
	for j in range(j_start, j_end):
		board[i][j] = number_placement[j-j_start]

def remove_numbers_from_row(i, j_start=0, j_end=n):
	for j in range(j_start, j_end):
		board[i][j] = -1

print_count = [0]
print_board()
def recurse(i=n-1):
	if print_count[0] == 50:
		print_count[0] = 0
		erase_lines(n+1)
		print_board()

	print_count[0] += 1

	if i == -1:
		erase_lines(n+1)
		print("SOLUTION")
		print_board()
		print_board()
		return

	for black_square_placement in get_black_square_placements_for_row(i):
		add_black_squares_to_row(black_square_placement, i)
		point_to_region_stack.append(get_point_to_region_mapping())
		for number_placement in get_number_placements_for_row(i):
			add_numbers_to_row(number_placement, i)
			recurse(i-1)
			remove_numbers_from_row(i)
		point_to_region_stack.pop()
		remove_black_squares_from_row(i)

recurse()
erase_lines(n+1)
