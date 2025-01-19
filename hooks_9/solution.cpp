#include <iostream>
#include <vector>
#include <iomanip>
#include <numeric>

class Solver {
	public:
		int *row_gcd;
		int *col_gcd;
		int **solution;
		int **board;
		int expected_solution[5][5] = {{0,4,4,4,0},
										{5,5,0,5,0},
										{3,0,0,5,4},
										{1,2,3,0,0},
										{2,0,3,5,0}};
		
		bool *seen_hooks;
		int seen_hooks_count = 0;
		int *hooks;
		
		int result_count = 0;
		int print_count = 0;

		static const int n = 9;
		// static const int n = 5;
		void solve() {
			row_gcd = new int[n]{55, 1, 6, 1, 24, 3, 6, 7, 2};
			col_gcd = new int[n]{5, 1, 6, 1, 8, 1, 22, 7, 8};
			hooks = new int[n]{9,8,7,6,5,4,3,2,1};
			// row_gcd = new int[n]{0, 5, 3, 123, 1};
			// col_gcd = new int[n]{0, 1, 1, 5, 4};
			// hooks = new int[n]{5,4,3,2,1};
			seen_hooks = new bool[n]{};
			board = new int*[n];
			solution = new int*[n];
			for (int i=0; i<n; ++i) {
				board[i] = new int[n]{};
				solution[i] = new int[n]{};
			}
			backtrack();
			std::cout << "result_count: " << result_count << std::endl;
			printSolution();
		}

		bool matches() {
			for (int i=0; i<n; i++) {
				for (int j=0; j<n; j++) {
					if (board[i][j] != 0 && board[i][j] != expected_solution[i][j]) {
						return false;
					}
				}
			}
			return true;
		}

		void printGrid(int** grid, bool clear_output) {
			std::cout << "    ";
			for (int j=0; j<n; j++) {
				std::string g = col_gcd[j] == 0 ? "" : std::to_string(col_gcd[j]);
				std::cout << std::setw(3) << g << " ";
			}
			std::cout << std::endl;
			for (int i=0; i<n; i++) {
				std::string g = row_gcd[i] == 0 ? "" : std::to_string(row_gcd[i]);
				std::cout << std::setw(3) << g;
				for (int j=0; j<n; j++) {
					std::string b = grid[i][j] == 0 ? "" : std::to_string(grid[i][j]);
					std::cout << std::setw(3) << b << " ";
				}
				std::cout << std::endl;
			}
			std::cout << std::endl;

			if (clear_output) {
				std::cout << "\033[" << (n+2) << "A";
			}
		}

		void printSolution() {
			printGrid(solution, false);
		}

		void printBoard() {
			printGrid(board, true);
		}

		void saveSolution() {
			for (int i=0; i<n; ++i) {
				for (int j=0; j<n; j++) {
					solution[i][j] = board[i][j];
				}
			}
		}

		bool twoByTwoRegionHasUnfilledSquare(int i, int j) {
			if (i > 0 && j > 0) {
				if (board[i][j-1] != 0 && board[i-1][j] != 0 && board[i-1][j-1] != 0) {
					return false;
				}
			}
			if (i > 0 && j < n-1) {
				if (board[i][j+1] != 0 && board[i-1][j] != 0 && board[i-1][j+1] != 0) {
					return false;
				}
			}
			if (i < n-1 && j > 0) {
				if (board[i][j-1] != 0 && board[i+1][j] != 0 && board[i+1][j-1] != 0) {
					return false;
				}
			}
			if (i < n-1 && j < n-1) {
				if (board[i][j+1] != 0 && board[i+1][j] != 0 && board[i+1][j+1] != 0) {
					return false;
				}
			}
			return true;
		}

		int array_gcd(std::vector<int>& a) {
			if (a.size() == 1) {
				return a[0];
			}
			int result = std::gcd(a[0], a[1]);
			for (int i=2; i<a.size(); ++i) {
				result = std::gcd(result, a[i]);
			}
			return result;
		}

		std::vector<int> parse_nums_from_col(int j) {
			std::vector<int> result;
			int current = 0;

			for (int i=0; i<n+1; ++i) {
				if (i == n || board[i][j] == 0) {
					if (current != 0) {
						result.push_back(current);
						current = 0;
					}
				} else {
					current = 10 * current + board[i][j];
				}
			}
			return result;
		}

		std::vector<int> parse_nums_from_row(int i) {
			std::vector<int> result;
			int current = 0;

			for (int j=0; j<n+1; ++j) {
				if (j == n || board[i][j] == 0) {
					if (current != 0) {
						result.push_back(current);
						current = 0;
					}
				} else {
					current = 10 * current + board[i][j];
				}
			}
			return result;
		}

		bool producesExpectedGcd(int dim, int i, int j) {
			int expected = dim == 0 ? row_gcd[i] : col_gcd[j];
			if (expected == 0) {
				return true;
			}
			std::vector<int> nums = dim == 0 ? parse_nums_from_row(i) : parse_nums_from_col(j);
			if (nums.size() == 0) {
				return false;
			}
			return array_gcd(nums) == expected;
		}

		bool respectsRowGcd(int i) {
			return producesExpectedGcd(0, i, -1);
		}

		bool respectsColGcd(int j) {
			return producesExpectedGcd(1, -1, j);
		}

		bool partiallyRespectsRowGcd(int i, int left, int right) {
			if (row_gcd[i] == 0 || row_gcd[i] == 1) {
				return true;
			}
			std::vector<int> confirmed_numbers;
			int current = 0;
			for (int j=0; j<left; ++j) {
				if (board[i][j] == 0) {
					if (current != 0) {
						confirmed_numbers.push_back(current);
						current = 0;
					}
				} else {
					current = 10 * current + board[i][j];
				}
			}
			current = 0;
			int j = right + 1;
			while (j<n && board[i][j] != 0) {
				++j; // ignore numbers that touch the right side of the unfilled board
			}
			for (; j<n; ++j) {
				if (board[i][j] == 0) {
					if (current != 0) {
						confirmed_numbers.push_back(current);
						current = 0;
					}
				} else {
					current = 10 * current + board[i][j];
				}
			}
			for (int number : confirmed_numbers) {
				if (number % row_gcd[i] != 0) {
					return false;
				}
			}
			return true;
		}

		bool partiallyRespectsColGcd(int j, int top, int bottom) {
			if (col_gcd[j] == 0 || col_gcd[j] == 1) {
				return true;
			}
			std::vector<int> confirmed_numbers;
			int current = 0;
			for (int i=0; i<top; ++i) {
				if (board[i][j] == 0) {
					if (current != 0) {
						confirmed_numbers.push_back(current);
						current = 0;
					}
				} else {
					current = 10 * current + board[i][j];
				}
			}
			current = 0;
			int i = bottom + 1;
			while (i<n && board[i][j] != 0) {
				++i; // ignore numbers that touch the right side of the unfilled board
			}
			for (; i<n; ++i) {
				if (board[i][j] == 0) {
					if (current != 0) {
						confirmed_numbers.push_back(current);
						current = 0;
					}
				} else {
					current = 10 * current + board[i][j];
				}
			}
			for (int number : confirmed_numbers) {
				if (number % col_gcd[j] != 0) {
					return false;
				}
			}
			return true;
		}

		bool connected(int top, int bottom, int left, int right) {
			std::vector<std::vector<bool>> visited(n, std::vector<bool>(n, false));
			int expected = 0;

			for (int i = 0; i < n; i++) {
				for (int j = 0; j < n; j++) {
					if (empty(i, j)) {
						continue;
					}
					expected += 1;
				}
			}

			int actual = 0;
			std::vector<std::pair<int, int>> queue;
			for (int i = top; i < bottom+1; ++i) {
				if (i < 0 || i > n - 1) {
					continue;
				}
				if (left > 0 && !empty(i, left - 1)) {
					queue.push_back(std::make_pair(i, left - 1));
				}
				if (right < n - 1 && !empty(i, right + 1)) {
					queue.push_back(std::make_pair(i, right + 1));
				}
			}

			for (int j = left - 1; j < right + 2; ++j) {
				if (j < 0 || j > n - 1) {
					continue;
				}
				if (top > 0 && !empty(top - 1, j)) {
					queue.push_back(std::make_pair(top - 1, j));
				}
				if (bottom < n - 1 && !empty(bottom + 1, j)) {
					queue.push_back(std::make_pair(bottom + 1, j));
				}
			}

			while (!queue.empty()) {
				std::vector<std::pair<int, int>> new_queue;
				for (auto& p : queue) {
					int i = p.first;
					int j = p.second;
					if (visited[i][j]) {
						continue;
					}
					visited[i][j] = true;
					actual += 1;
					
					if (i > 0 && !empty(i - 1, j)) {
						new_queue.push_back(std::make_pair(i - 1, j));
					}
					if (i < n - 1 && !empty(i + 1, j)) {
						new_queue.push_back(std::make_pair(i + 1, j));
					}
					if (j > 0 && !empty(i, j - 1)) {
						new_queue.push_back(std::make_pair(i, j - 1));
					}
					if (j < n - 1 && !empty(i, j + 1)) {
						new_queue.push_back(std::make_pair(i, j + 1));
					}
				}
				queue = new_queue;
			}
			return actual == expected;
		}

		bool empty(int i, int j) {
			return board[i][j] == 0;
		}

		void backtrack(int top = 0, int bottom = n - 1, int left = 0, int right = n - 1,
					int row_i = -1, int col_j = -1, int i_min = -1, int i_max = -1, int j_min = -1, int j_max = -1,
					int hook = -1, int count = 0) {
			if (count == 0) {
				if (row_i != -1 && (!respectsRowGcd(row_i) || !respectsColGcd(col_j))) {
					return;
				}
				if (left > 1 || n - 1 - right > 1) {
					for (int j = left; j <= right; j++) {
						if (!partiallyRespectsColGcd(j, top, bottom)) {
							return;
						}
					}
				}
				if (!connected(top, bottom, left, right)) {
					return;
				}
				if (seen_hooks_count == n) {
					saveSolution();
					printSolution();
					std::cout << "SOLUTION!!!" << std::endl;
					result_count += 1;
					return;
				}
				print_count += 1;
				if (print_count == 100) {
					printBoard();
					print_count = 0;
				}
				for (int hook_index = 0; hook_index<n; ++hook_index) {
					int new_hook = hooks[hook_index];
					if (seen_hooks[new_hook]) {
						continue;
					}
					seen_hooks[new_hook] = true;
					seen_hooks_count += 1;
					if (seen_hooks_count < n) {
						backtrack(top+1, bottom, left+1, right,  top, left,      top, bottom, left+1, right, new_hook, new_hook);
						backtrack(top, bottom-1, left+1, right,  bottom, left,   top, bottom, left+1, right, new_hook, new_hook);
						backtrack(top+1, bottom, left, right-1,  top, right,     top, bottom, left, right-1, new_hook, new_hook);
						backtrack(top, bottom-1, left, right-1,  bottom, right,  top, bottom, left, right-1, new_hook, new_hook);
					} else {
						backtrack(top+1, bottom, left+1, right,  top, left,      top, bottom, left+1, right, new_hook, new_hook);
					}
					seen_hooks_count -= 1;
					seen_hooks[new_hook] = false;
				}
				return;
			}

			if (i_min < i_max + 1) {
				if ((i_max - i_min + 1) + (j_max - j_min + 1) < count) {
					return;
				}
			} else {
				if ((j_max - j_min + 1) < count) {
					return;
				}
			}
			

			if (i_min == i_max + 1) {
				if (!respectsColGcd(col_j)) {
					return;
				}
				if (top > 1 || n - 1 - bottom > 1) {
					for (int i = top; i <= bottom; i++) {
						if (!partiallyRespectsRowGcd(i, left, right)) {
							return;
						}
					}
				}
			}

			for (int i = i_min; i < i_max + 1; ++i) {
				if (!twoByTwoRegionHasUnfilledSquare(i, col_j)) {
					continue;
				}
				board[i][col_j] = hook;
				backtrack(top, bottom, left, right, row_i, col_j, i + 1, i_max, j_min, j_max, hook, count - 1);
				board[i][col_j] = 0;
			}

			for (int j = j_min; j < j_max + 1; j++) {
				if (!twoByTwoRegionHasUnfilledSquare(row_i, j)) {
					continue;
				}
				board[row_i][j] = hook;
				backtrack(top, bottom, left, right, row_i, col_j, i_max + 2, i_max, j + 1, j_max, hook, count - 1);
				board[row_i][j] = 0;
			}
		}
};

int main() {
	Solver solver = Solver();
	solver.solve();
}
