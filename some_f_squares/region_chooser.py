import getch

current_i, current_j = (0, 0)
current_region = []
regions = []

n = 17

colors = ["🟪", "🟫", "🟥", "🟨", "🟧", "🟦"]

def get_color(i, j):
	if (i, j) == (current_i, current_j):
		return "🟩"
	if (i, j) in current_region:
		return "⬛"
	for idx, region in enumerate(regions):
		if (i, j) in region:
			return colors[idx % len(colors)]
	return "⬜"

def print_board():
	for i in range(n):
		for j in range(n):
			print(get_color(i, j), end="")
		print("")

def erase_lines(n):
	for _ in range(n):
		print("\033[A\033[K", end="")

print_board()
erase_lines(n)
while True:
	key = getch.getch().lower()
	if key == "w":
		current_i -= 1
	elif key == "s":
		current_i += 1
	elif key == "a":
		current_j -= 1
	elif key == "d":
		current_j += 1
	elif key == " ":
		current_region += [(current_i, current_j)]
	elif key == "p":
		erase_lines(len(regions))
		regions.append(current_region[:])
		current_region = []
		print("\n".join([str(region) for region in regions]))
	print_board()
	erase_lines(n)