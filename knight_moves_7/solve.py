#!/usr/bin/env python3
"""
Backtracking solver for the 3D-knight / pentomino-tower score puzzle.
"""
import sys

# ---------------------------------------------------------------------------
# Board data (parsed from board.png)
# ---------------------------------------------------------------------------

# Region id for each cell (13 regions: 12 pentominoes + one 2x2)
REGION = [
	[ 0,  0,  0,  0,  0,  1,  1, 1],
	[ 2,  2,  2,  3,  3,  4,  4, 1],
	[ 2,  5,  2,  3,  3,  3,  4, 1],
	[ 6,  5,  5,  7,  7,  8,  4, 4],
	[ 6,  6,  5,  7,  7,  8,  8, 9],
	[ 6, 10,  5, 11,  8,  8, 12, 9],
	[ 6, 10, 11, 11, 11, 12, 12, 9],
	[10, 10, 10, 11, 12, 12,  9, 9],
]

NREG = 13
REGION_CELLS: list[list[tuple[int, int]]] = [[] for _ in range(NREG)]
for r in range(8):
	for c in range(8):
		REGION_CELLS[REGION[r][c]].append((r, c))

# Known scores written on the grid (r, c) -> score
SCORES: dict[tuple[int, int], int] = {
	(0, 5): 37,
	(0, 7): 1100,
	(2, 3): 23,
	(2, 5): 138,
	(3, 0): 528,
	(4, 1): 449,
	(4, 4): 16,
	(5, 1): 750,
	(5, 3): 88,
	(5, 5): 272,
	(5, 6): 1,
	(7, 0): 0,  # start
}

START = (7, 0)
LABELED = set(SCORES.keys())
# Non-start labeled cells (write targets)
WRITE_CELLS = [p for p in SCORES if p != START]

# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def in_bounds(r: int, c: int) -> bool:
	return 0 <= r < 8 and 0 <= c < 8


def knight_deltas_2d():
	"""All (dr, dc, |dh| required) possibilities for a 3D knight move.

	Heights only differ by 0 or 1, so |dh| is 0 or 1 (never 2).
	- same height (|dh|=0): classic knight (|dr|,|dc|) in {(1,2),(2,1)}
	- height change 1:     (|dr|,|dc|) in {(0,2),(2,0)}
	"""
	out = []
	# same height
	for dr, dc in ((1, 2), (1, -2), (-1, 2), (-1, -2),
				   (2, 1), (2, -1), (-2, 1), (-2, -1)):
		out.append((dr, dc, 0))  # |dh| must be 0
	# height changes by 1
	for dr, dc in ((0, 2), (0, -2), (2, 0), (-2, 0)):
		out.append((dr, dc, 1))  # |dh| must be 1
	return out


DELTAS = knight_deltas_2d()


def neighbors_any(r: int, c: int):
	"""Possible destination cells ignoring height (may or may not be valid)."""
	for dr, dc, dhrex in DELTAS:
		nr, nc = r + dr, c + dc
		if in_bounds(nr, nc):
			yield nr, nc, dhrex


# ---------------------------------------------------------------------------
# Score update
# ---------------------------------------------------------------------------

def apply_score(score: int, move_n: int, h_from: int, h_to: int):
	"""Return new score after move_n, or None if move illegal (down not divisible)."""
	if h_to == h_from:
		return score + move_n
	if h_to > h_from:
		return score * move_n
	# down
	if move_n == 0 or score % move_n != 0:
		return None
	return score // move_n


# ---------------------------------------------------------------------------
# Write-move schedule
# ---------------------------------------------------------------------------

def make_write_moves(K: int, max_moves: int) -> set[int]:
	s = {3, 6, 9, 12, 15, 18}
	t = 18 + K
	while t <= max_moves:
		s.add(t)
		t += K
	return s


# ---------------------------------------------------------------------------
# Backtracking search
# ---------------------------------------------------------------------------

class Solver:
	def __init__(self, K: int):
		self.K = K
		# Max path length: 64 cells => 63 moves. Last write at 18+5K must fit.
		self.max_moves = 63
		last_write = 18 + 5 * K
		if last_write > self.max_moves:
			raise ValueError(f"K={K} last write {last_write} too large")
		# We need exactly 11 write events for 11 labeled non-start cells.
		# Write moves: 6 fixed + 5 more at 18+K..18+5K
		self.required_writes = sorted(
			list({3, 6, 9, 12, 15, 18}) + [18 + i * K for i in range(1, 6)]
		)
		assert len(self.required_writes) == 11
		self.write_set = set(self.required_writes)
		# Path must be long enough to include last write; may continue a bit.
		self.min_moves = self.required_writes[-1]  # at least
		# After last write, may need more moves to hit remaining towers.
		# Absolute max is 63.

		# tower_of_region[rid] = cell with tower, or None if undecided
		# -1 means "decided no tower here yet" tracked via placement
		self.tower: list[tuple[int, int] | None] = [None] * NREG  # placed tower cell
		# For each region, whether tower is placed
		self.tower_placed = [False] * NREG

		self.visited = [[False] * 8 for _ in range(8)]
		self.path: list[tuple[int, int]] = []
		self.path_scores: list[int] = []  # score upon arrival (index 0 = start)

		self.solutions = []
		self.nodes = 0
		self.pruned = 0

		# Precompute which labeled cell has which score for reverse lookup
		self.score_to_cell = {v: p for p, v in SCORES.items() if p != START}

		# Height of cell: 2 if tower there, 1 otherwise.
		# Only known if region tower is placed.
		# For unplaced regions, height is ambiguous (1 or 2) unless forced.

	def height(self, r: int, c: int) -> int | None:
		"""Return height if known, else None."""
		rid = REGION[r][c]
		if not self.tower_placed[rid]:
			return None
		return 2 if self.tower[rid] == (r, c) else 1

	def try_place_tower(self, r: int, c: int, want_h: int) -> bool:
		"""
		Try to make cell (r,c) have height want_h (1 or 2).
		Returns True if consistent (and records placement if newly decided).
		Returns False if contradiction.
		On success, caller must undo via undo stack if we placed something.
		Actually returns ('ok', undo_info) or ('fail', None).
		"""
		rid = REGION[r][c]
		if self.tower_placed[rid]:
			actual = 2 if self.tower[rid] == (r, c) else 1
			return actual == want_h, None
		# Not yet placed
		if want_h == 2:
			self.tower[rid] = (r, c)
			self.tower_placed[rid] = True
			return True, (rid, True)  # placed tower here
		else:
			# want height 1: cell is NOT the tower. Don't place yet unless
			# this is the last free cell in region.
			# Just leave undecided - but we need height 1 for THIS cell now.
			# Record that this cell is forbidden as tower? Or place tower elsewhere later.
			# For correctness with current move, we only need this cell h=1.
			# Mark cell as "not tower" by... we need a forbidden set, OR
			# we force-place tower on this cell only when want_h=2;
			# when want_h=1, we mark cell excluded.
			return True, ("exclude", rid, r, c)

	def solve(self):
		# Start cell height: try both (tower or not)
		for start_h in (1, 2):
			self._reset()
			rid = REGION[START[0]][START[1]]
			self.tower[rid] = START if start_h == 2 else None
			self.tower_placed[rid] = start_h == 2
			# If start_h == 1, region still unplaced; start is excluded from being tower
			excluded = set()
			if start_h == 1:
				excluded.add(START)

			self.visited[START[0]][START[1]] = True
			self.path = [START]
			self.path_scores = [0]
			towers_hit = 1 if start_h == 2 else 0

			self._dfs(
				r=START[0],
				c=START[1],
				score=0,
				move=0,
				towers_hit=towers_hit,
				excluded=excluded,
				writes_done=0,
			)
			if self.solutions:
				return self.solutions
		return self.solutions

	def _reset(self):
		self.tower = [None] * NREG
		self.tower_placed = [False] * NREG
		self.visited = [[False] * 8 for _ in range(8)]
		self.path = []
		self.path_scores = []

	def _dfs(self, r, c, score, move, towers_hit, excluded, writes_done):
		self.nodes += 1
		if self.nodes % 500000 == 0:
			print(
				f"  [K={self.K}] nodes={self.nodes} depth={move} "
				f"towers={towers_hit}/13 writes={writes_done}/11 score={score}",
				file=sys.stderr,
			)

		# Path ends exactly when the last tower is visited.
		if towers_hit == 13:
			if writes_done == 11 and all(self.tower_placed):
				self.solutions.append(self._snapshot())
				return True
			# Path must stop here but writes incomplete, or towers not all placed
			return False

		# All writes done but still need towers — keep going
		if move >= self.max_moves:
			return False

		next_move = move + 1
		is_write = next_move in self.write_set

		remaining_writes = 11 - writes_done
		if remaining_writes > 0:
			next_w = self.required_writes[writes_done]
			if next_move > next_w:
				return False  # missed a write move
		else:
			# no more writes allowed — must not land on write schedule
			if is_write:
				# schedule has a write but we already wrote 11 times — shouldn't happen
				# if write_set only has 11 entries
				pass

		h_from = self._forced_height(r, c, excluded)
		if h_from is None:
			raise RuntimeError(f"unknown height on path at {(r,c)} excl={excluded}")

		# Build candidates
		candidates = []
		if is_write:
			for (nr, nc) in WRITE_CELLS:
				if self.visited[nr][nc]:
					continue
				dr, dc = nr - r, nc - c
				adh_needed = None
				for ddr, ddc, dhrex in DELTAS:
					if ddr == dr and ddc == dc:
						adh_needed = dhrex
						break
				if adh_needed is None:
					continue
				candidates.append((nr, nc, adh_needed))
		else:
			for nr, nc, adh_needed in neighbors_any(r, c):
				if self.visited[nr][nc]:
					continue
				if (nr, nc) in LABELED:
					continue
				candidates.append((nr, nc, adh_needed))

		for nr, nc, adh_needed in candidates:
			if adh_needed == 0:
				possible_h_to = [h_from]
			else:
				possible_h_to = [h for h in (1, 2) if abs(h - h_from) == 1]

			for h_to in possible_h_to:
				new_score = apply_score(score, next_move, h_from, h_to)
				if new_score is None:
					continue

				if is_write and SCORES.get((nr, nc)) != new_score:
					continue

				ok, undo = self._enforce_height(nr, nc, h_to, excluded)
				if not ok:
					continue

				self.visited[nr][nc] = True
				self.path.append((nr, nc))
				self.path_scores.append(new_score)

				new_towers = towers_hit + (1 if h_to == 2 else 0)
				new_writes = writes_done + (1 if is_write else 0)
				new_excluded = excluded | {(nr, nc)} if (undo and undo[0] == "exclude") else excluded

				# Prune: remaining towers cannot exceed remaining non-excluded capacity;
				# also if towers still needed after we'd be forced to stop at last write+...
				# Must be able to hit remaining writes before finishing towers, or together.
				remaining_towers = 13 - new_towers
				# Cells still available
				# Soft prune: if no remaining writes and remaining towers, need moves

				found = self._dfs(
					nr, nc, new_score, next_move, new_towers, new_excluded, new_writes
				)

				self.path.pop()
				self.path_scores.pop()
				self.visited[nr][nc] = False
				self._undo_enforce(undo)

				if found:
					return True

		return False

	def _forced_height(self, r, c, excluded) -> int | None:
		rid = REGION[r][c]
		if self.tower_placed[rid]:
			return 2 if self.tower[rid] == (r, c) else 1
		if (r, c) in excluded:
			return 1
		return None  # undecided

	def _enforce_height(self, r, c, want_h, excluded):
		"""
		Force cell (r,c) to have height want_h.
		Returns (ok, undo_token).
		"""
		rid = REGION[r][c]
		if (r, c) in excluded and want_h == 2:
			return False, None

		if self.tower_placed[rid]:
			actual = 2 if self.tower[rid] == (r, c) else 1
			return (actual == want_h), None

		# Region undecided
		if want_h == 2:
			# Place tower here - only if not excluded
			# Also all other visited cells in region must not need to be towers
			# (they're already height 1 effectively)
			self.tower[rid] = (r, c)
			self.tower_placed[rid] = True
			return True, ("place", rid)

		# want_h == 1: exclude this cell as tower location
		# If all other cells in region are excluded or... check if only this left
		# Count free cells in region that could still hold tower
		free = []
		for (rr, cc) in REGION_CELLS[rid]:
			if (rr, cc) in excluded:
				continue
			if (rr, cc) == (r, c):
				continue
			free.append((rr, cc))
		# Also if some unvisited cells exist they can hold tower
		# free currently = other non-excluded cells (visited or not)
		if not free:
			# No place left for tower - contradiction unless we can place later
			# No other cell can take the tower
			return False, None
		# Just exclude this cell
		return True, ("exclude", rid, r, c)

	def _undo_enforce(self, undo):
		if undo is None:
			return
		if undo[0] == "place":
			rid = undo[1]
			self.tower[rid] = None
			self.tower_placed[rid] = False
		# exclude is only in the excluded set passed by value (new set), no undo needed

	def _finalize_towers(self, excluded) -> bool:
		"""Place remaining towers on visited cells of unplaced regions."""
		for rid in range(NREG):
			if self.tower_placed[rid]:
				continue
			# Tower must be visited (path visits all towers)
			candidates = [
				(r, c)
				for (r, c) in REGION_CELLS[rid]
				if self.visited[r][c] and (r, c) not in excluded
			]
			if not candidates:
				return False
			# Pick first candidate (any is fine for answer? heights affect path
			# already done - wait, if region unplaced, all path cells in region
			# were treated as height 1 (excluded or assumed). So tower must be
			# on a visited cell that was used as height 1 - CONTRADICTION.
			# Actually if we used h=1 for a cell, it's excluded. If we never
			# visited any cell as h=2, we can't place tower on path with h=2.
			# So unplaced regions at the end mean we visited cells as h=1 only,
			# and tower would need h=2 - impossible for path consistency.
			# Therefore all towers must be placed during search.
			return False
		return True

	def _snapshot(self):
		heights = [[1] * 8 for _ in range(8)]
		for rid in range(NREG):
			if self.tower[rid]:
				tr, tc = self.tower[rid]
				heights[tr][tc] = 2
		return {
			"K": self.K,
			"path": list(self.path),
			"scores": list(self.path_scores),
			"towers": [self.tower[rid] for rid in range(NREG)],
			"heights": heights,
			"nodes": self.nodes,
		}


def compute_answer(sol):
	"""Sum of neighbor-sums of unvisited squares."""
	path = sol["path"]
	scores = sol["scores"]
	score_at = {cell: sc for cell, sc in zip(path, scores)}
	visited = set(path)
	total = 0
	details = []
	for r in range(8):
		for c in range(8):
			if (r, c) in visited:
				continue
			nsum = 0
			for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
				nr, nc = r + dr, c + dc
				if (nr, nc) in score_at:
					nsum += score_at[(nr, nc)]
			details.append(((r, c), nsum))
			total += nsum
	return total, details


def main():
	# Try K values from 4 upward
	for K in range(4, 10):
		last = 18 + 5 * K
		if last > 63:
			print(f"Skipping K={K}, last write={last}")
			continue
		print(f"\n=== Trying K={K} (writes at {sorted(list({3,6,9,12,15,18}|set(18+i*K for i in range(1,6))))}) ===")
		solver = Solver(K)
		sols = solver.solve()
		print(f"K={K}: nodes={solver.nodes}, solutions={len(sols)}")
		if sols:
			sol = sols[0]
			ans, details = compute_answer(sol)
			print("PATH:")
			for i, (cell, sc) in enumerate(zip(sol["path"], sol["scores"])):
				mark = ""
				if i in solver.write_set or i == 0:
					mark = " WRITE" if i else " START"
				print(f"  move {i:2d}: {cell} score={sc}{mark}")
			print("TOWERS:", sol["towers"])
			print("ANSWER:", ans)
			print("Unvisited neighbor sums:", details)
			return ans
	print("No solution found")
	return None


if __name__ == "__main__":
	main()
