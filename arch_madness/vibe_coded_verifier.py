def verify_solution(score_grid, arc_grid):
	N = len(score_grid)
	UP_DIR = 0
	RIGHT_DIR = 1
	DOWN_DIR = 2
	LEFT_DIR = 3
	parent = [i for i in range(N * N * 4)]

	def find(i):
		if parent[i] == i:
			return i
		parent[i] = find(parent[i])
		return parent[i]

	def union(i, j):
		root_i = find(i)
		root_j = find(j)
		if root_i != root_j:
			parent[root_i] = root_j

	def get_node(r, c, pos):
		# pos indices: 0=Top, 1=Right, 2=Bottom, 3=Left
		return r * N * 4 + c * 4 + pos

	# 1. Build basic connected components
	for r in range(N):
		for c in range(N):
			arc = arc_grid[r][c]
			top = get_node(r, c, UP_DIR)
			right = get_node(r, c, RIGHT_DIR)
			bottom = get_node(r, c, DOWN_DIR)
			left = get_node(r, c, LEFT_DIR)

			# Internal cell connections
			if arc == "_":
				union(top, right)
				union(right, bottom)
				union(bottom, left)
			elif arc in ["TL", "BR"]:
				union(top, left)
				union(bottom, right)
			elif arc in ["TR", "BL"]:
				union(top, right)
				union(bottom, left)

	# 2. Connect components across adjacent cell boundaries
	for r in range(N):
		for c in range(N):
			if r > 0:
				union(get_node(r, c, UP_DIR), get_node(r-1, c, DOWN_DIR))
			if c > 0:
				union(get_node(r, c, LEFT_DIR), get_node(r, c-1, RIGHT_DIR))

	# 3. Categorize pieces per region and check rules
	region_full = {}
	region_inside = {}
	region_outside = {}
	for i in range(N * N * 4):
		region_full[i] = 0
		region_inside[i] = 0
		region_outside[i] = 0

	for r in range(N):
		for c in range(N):
			arc = arc_grid[r][c]
			top = get_node(r, c, UP_DIR)
			bottom = get_node(r, c, DOWN_DIR)

			if arc == "_":
				region_full[find(top)] += 1
			else:
				if arc in ["TL", "TR"]:
					in_comp, out_comp = find(top), find(bottom)
				elif arc in ["BL", "BR"]:
					in_comp, out_comp = find(bottom), find(top)

				if in_comp == out_comp:
					print(f"❌ Error: Arc at row {r}, col {c} is 'dangling' (it fails to divide the grid; both sides belong to the same region).")
					return False

				region_inside[in_comp] += 1
				region_outside[out_comp] += 1

	all_comps = set(find(i) for i in range(N * N * 4))
	region_area = {}

	# 4. Resolve exact area and check the "integer area" criteria
	for comp in all_comps:
		if region_inside[comp] != region_outside[comp]:
			print(f"❌ Error: Region {comp} has an irrational area. Inside Arcs: {region_inside[comp]} != Outside Arcs: {region_outside[comp]}")
			return False
		# Every inside + outside pair equals exactly 1.0 area. 
		region_area[comp] = region_full[comp] + region_outside[comp]

	# 5. Extract boundary vector paths for 'Smooth Perimeter' calculation
	region_pieces = {comp: [] for comp in all_comps}
	
	for r in range(N):
		for c in range(N):
			arc = arc_grid[r][c]
			top = get_node(r, c, UP_DIR)
			bottom = get_node(r, c, DOWN_DIR)
			left = get_node(r, c, LEFT_DIR)
			right = get_node(r, c, RIGHT_DIR)

			# Outer grid edges
			# Format: (start_point, end_point, entry_tangent, exit_tangent)
            # We trace counter-clockwise (keeping the region's inside strictly to our left).
			if r == 0:
				# (c+1 to c) with a movement vector of (-1, 0) moving purely leftwards.
				region_pieces[find(top)].append(((c+1, 0), (c, 0), (-1, 0), (-1, 0)))
			if r == N-1:
				region_pieces[find(bottom)].append(((c, N), (c+1, N), (1, 0), (1, 0)))
			if c == 0:
				region_pieces[find(left)].append(((0, r), (0, r+1), (0, 1), (0, 1)))
			if c == N-1:
				region_pieces[find(right)].append(((N, r+1), (N, r), (0, -1), (0, -1)))

			# Directed inner arcs (Tracking point-to-point tangents keeping bounded region exclusively to the Left)
			if arc == "TL":
				in_comp, out_comp = find(top), find(bottom)
				region_pieces[in_comp].append(((c, r+1), (c+1, r), (1, 0), (0, -1)))
				region_pieces[out_comp].append(((c+1, r), (c, r+1), (0, 1), (-1, 0)))
			elif arc == "TR":
				in_comp, out_comp = find(top), find(bottom)
				region_pieces[in_comp].append(((c, r), (c+1, r+1), (0, 1), (1, 0)))
				region_pieces[out_comp].append(((c+1, r+1), (c, r), (-1, 0), (0, -1)))
			elif arc == "BL":
				in_comp, out_comp = find(bottom), find(top)
				region_pieces[in_comp].append(((c+1, r+1), (c, r), (0, -1), (-1, 0)))
				region_pieces[out_comp].append(((c, r), (c+1, r+1), (1, 0), (0, 1)))
			elif arc == "BR":
				in_comp, out_comp = find(bottom), find(top)
				region_pieces[in_comp].append(((c+1, r), (c, r+1), (-1, 0), (0, 1)))
				region_pieces[out_comp].append(((c, r+1), (c+1, r), (0, -1), (1, 0)))

	# 6. Cycle building & determining total score metric
	region_score = {}
	for comp in all_comps:
		pieces = region_pieces[comp]
		adj = {}
		for p in pieces:
			if p[0] in adj:
				print(f"❌ Error: Graph fault for region boundary tracking. Invalid loop state traced around {p[0]}")
				return False
			adj[p[0]] = p

		num_smooth = 0
		visited = set()

		for p in pieces:
			if p[0] not in visited:
				curr = p
				loop_kinks = 0
				while True:
					visited.add(curr[0])
					nxt = adj.get(curr[1])
					if not nxt:
						print(f"❌ Error: Geometrical perimeter breakdown, loop trace detached at grid node {curr[1]}")
						return False

					# If leaving tangent differs from encountering tangent, you have a discrete geometrical kink.
					if curr[3] != nxt[2]:
						loop_kinks += 1

					curr = nxt
					if curr[0] == p[0]:
						break

				# A fully clean loop with 0 kinks structurally makes exactly 1 "smooth piece"
				num_smooth += max(1, loop_kinks)

		region_score[comp] = region_area[comp] * num_smooth

	# 7. Final comparison check against Score Grid
	for r in range(N):
		for c in range(N):
			arc = arc_grid[r][c]

			# Extract the Region Component which encapsulates the >50% Area of the targeted cell bounds.
			if arc == "_" or arc == "TL" or arc == "TR":
				maj_comp = find(get_node(r, c, UP_DIR))
			else:
				maj_comp = find(get_node(r, c, DOWN_DIR))

			expected = score_grid[r][c]
			actual = region_score[maj_comp]

			if expected != actual:
				print(f"❌ Verification Mismatch at Row {r}, Col {c} | Expected Puzzle Score: {expected} | Actual Calculated Region Score: {actual}")
				return False

	print("✅ Verification passed! All regions are cleanly bound, possess structurally validated integer areas, and match the final score calculations.")
	return True

# --- Input Grids ---
score_grid = [
	[ 21,  21,  21,  27,  27, 288, 288,  15,  25],
	[ 21,  21,  21,  27,  27,  15,  15,  25,  25],
	[ 21,  27,  27, 288, 288,  15,  15,  25,   9],
	[ 25,  27,  27, 288, 288,  45,  45,  25,   9],
	[ 25,  25,  25,  27, 288,  45,  45,  45,   9],
	[288,  25, 288,  63, 288, 288, 288,  45,  45],
	[  9,   9,  63,  63, 288,  35,  35,  45,  45],
	[  9,  63,  63, 288,   9,   9,  35, 288, 288],
	[ 63,  63, 288, 288,   9,  35,  35,  35,  35]
]

arc_grid = [
	[ '_',  '_', 'BL',  '_', 'BL',  '_', 'TL',  '_', 'BR'],
	[ '_',  '_', 'TL',  '_', 'TL', 'BR',  '_', 'BR',  '_'],
	[ '_', 'BR',  '_', 'BR', 'TL', 'TR', 'TL',  '_', 'BR'],
	['BR', 'TR',  '_', 'TR', 'BL',  '_', 'BL', 'TL',  '_'],
	[ '_',  '_', 'BL', 'TL',  '_', 'TR',  '_', 'BL', 'TL'],
	['BR', 'TR', 'BR', 'BR', 'TR',  '_', 'BL',  '_',  '_'],
	['BR', 'BL', 'BR',  '_', 'BR', 'BR', 'BL', 'TR', 'TL'],
	[ '_', 'BR',  '_', 'BR', 'BR', 'BL',  '_', 'TR', 'TL'],
	['BR',  '_', 'BR', 'TL',  '_', 'BR',  '_',  '_',  '_']
]

verify_solution(score_grid, arc_grid)

N = len(score_grid)
answer = (sum(sum(score_grid[i][j] for i in range(N))**2 for j in range(N)) +
		sum(sum(score_grid[i][j] for j in range(N))**2 for i in range(N)))
print(answer)