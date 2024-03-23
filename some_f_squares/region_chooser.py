current_i, current_j = (0, 0)
region = []

n = 17

def print_board():
	for i in range(n):
		for j in range(n):
			if (i, j) == (current_i, current_j):
				print("🟩", end="")
			elif (i, j) in region:
				print("⬛", end="")
			else:
				print("⬜", end="")
		print("")

while True:
	print_board()
	key = input()
	if key == "w":
		current_i -= 1
	elif key == "s":
		current_i += 1
	elif key == "a":
		current_j -= 1
	elif key == "d":
		current_j += 1
	elif key == " ":
		region += [(current_i, current_j)]
	elif key == "p":
		print(region)
		region = []
