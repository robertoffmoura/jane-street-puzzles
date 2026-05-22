import math

n = 13 # size of the board

grid_expressions = {
	# Row 0
	(0, 4): lambda a, b, c: 6*c - 4*b,

	# Row 1
	(1, 7): lambda a, b, c: 8 - b,

	# Row 2
	(2, 1): lambda a, b, c: (a**b - 4) / (6*c + 1),
	(2, 3): lambda a, b, c: (b + c) / (c - 1),
	(2, 6): lambda a, b, c: b**2 - (b / c),
	(2, 8): lambda a, b, c: math.sqrt(30 + a) / c,
	(2, 10): lambda a, b, c: (a + b) / (c - 3*a),

	# Row 3
	(3, 4): lambda a, b, c: (b - 3*a) / (a - c),
	(3, 7): lambda a, b, c: 8*a - 2*b,
	(3, 9): lambda a, b, c: b / (a - c),
	(3, 11): lambda a, b, c: (b + 9) / math.sqrt(c - a),

	# Row 4
	(4, 1): lambda a, b, c: 18 / (a * c + 1),
	(4, 5): lambda a, b, c: c**b,
	(4, 10): lambda a, b, c: (3 + b**2) / math.sqrt(3 + 2*c),

	# Row 5
	(5, 3): lambda a, b, c: b / (a**2 - c**2),
	(5, 12): lambda a, b, c: math.sqrt(a + 2) / a,

	# Row 6
	(6, 2): lambda a, b, c: a**b - 12 / a,
	(6, 4): lambda a, b, c: 2*c + (c / a),
	(6, 6): lambda a, b, c: 4*a - 5*b,
	(6, 8): lambda a, b, c: c + 2*a,
	(6, 10): lambda a, b, c: b / (9*a - 5*c),

	# Row 7
	(7, 0): lambda a, b, c: (b**3 + 2*c) / (b + 2*c),
	(7, 9): lambda a, b, c: b / (a - 1),

	# Row 8
	(8, 2): lambda a, b, c: (c - b) / (2 * a),
	(8, 7): lambda a, b, c: b / (a - c),
	(8, 11): lambda a, b, c: (b + c) / (a - c),

	# Row 9
	(9, 1): lambda a, b, c: math.log(a, c),
	(9, 3): lambda a, b, c: (c**2 - b) / a,
	(9, 5): lambda a, b, c: (b - 1)**2,
	(9, 8): lambda a, b, c: (43 - a * c)**(1/3) / a,

	# Row 10
	(10, 2): lambda a, b, c: (b - a) / (a - c),
	(10, 4): lambda a, b, c: 11 - b,
	(10, 6): lambda a, b, c: (b - 2*a) / (a - c),
	(10, 9): lambda a, b, c: (c + 3) / a,
	(10, 11): lambda a, b, c: 8*c - (b / c),

	# Row 11
	(11, 5): lambda a, b, c: b**2,

	# Row 12
	(12, 8): lambda a, b, c: (2**b + 1) / (a * c)
}

# 17 is the limit for N because 18 k-ominos wouldn't fit in the board: 1 + 2 ... + 18 > 13**2
n_limit = 17

# The cell with 8 - b must be in [1, 2, ... 17], so b is an integer in the range [-9, -8, ... 7]
# The cell with 11 - b must be in [1, 2, ... 17], so b is an integer in the range [-6, -8, ... 10]
# The cell with b**2 must be in [1, 2, ... 17], so b is in [-4, -3, -2, -1, 1, 2, 3, 4]
# The cell with (b-1)**2 must be in [1, 2, ... 17], so b is in [-3, -2, -1, 0, 2, 3, 4, 5]

# The 4 previous conditions mean b must be in [-3, -2, -1, 2, 3, 4]
possible_b_values = [-3, -2, -1, 2, 3, 4]

c_constraints = [
	lambda b,s: (s+4*b)/6,
	lambda b,s: 1+(b+1)/(s-1) if s != 1 else float("inf"),
	lambda b,s: b/(b**2 - s) if b**2 - s != 0 else float("inf"),
	lambda b,s: s**(1/b),
	lambda b,s: 0.5*(((3+b**2)/s)**2 - 3),
	lambda b,s: 0.5*((b**3-b)/(s-1) - b) if s != 1 else float("inf")
]

def intersect(list_of_lists):
	result = []
	first = list_of_lists[0]
	for e in first:
		if all(e in list_of_lists[i] for i in range(1, len(list_of_lists))):
			result.append(e)
	return result

for b in possible_b_values:
	c_values = []
	for constraint in c_constraints:
		# s is the value of the cell
		current = [constraint(b,s) for s in range(1,n_limit+1)]
		c_values.append(current)
	intersection = intersect(c_values)
	print(f"if b is {b}, then c must be in : " + ", ".join(f"{e:.3f}" for e in intersection))

# The only solution to the above is b = -3 and c = 0.5
b = -3
c = 0.5

a_constraints = [
	lambda b, c, s: (s * (6 * c + 1) + 4)**(1 / b),
	lambda b, c, s: (s * c)**2 - 30,
	lambda b, c, s: (s * c - b) / (1 + 3 * s),
	lambda b, c, s: (b + s * c) / (s + 3),
	lambda b, c, s: (s + 2 * b) / 8,
	lambda b, c, s: (b / s) + c,
	lambda b, c, s: c - ((b + 9) / s)**2 # and more...
]

a_values = []
for constraint in a_constraints:
	# s is the value of the cell
	current = [constraint(b,c,s) for s in range(1,n_limit+1)]
	a_values.append(current)
intersection = intersect(a_values)
print(f"a must be in : " + ", ".join(f"{e:.3f}" for e in intersection))

# Only one solution for a:
a = 0.25
