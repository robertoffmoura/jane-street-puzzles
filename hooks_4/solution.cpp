#include <iostream>
#include <iomanip>
#include <functional>
#include <queue>

const int n = 9;
int col_product[n] = {28, 552, 64, 15, 86, 1304, 170, 81, 810};
int row_product[n] = {810, 585, 415, 92, 67, 136, 8, 225, 567};
// const int n = 4;
// int col_product[n] = {16, 3, 0, 8};
// int row_product[n] = {20, 5, 0, 3};

int board[n][n]; // 0 means unvisited and -1 means visited and empty on purpose.
int solution[n][n];

int solution_count = 0;
int print_count = 0;

std::string format(int n) {
	// return (n == 0) ? " " : std::to_string(n);
	return (n == 0 || n == -1) ? " " : std::to_string(n);
}

void printGrid(int (*grid)[n][n]) {
	std::cout << "    ";
	for (int j=0; j<n; j++) {
		std::cout << std::setw(5) << format(col_product[j]);
	}
	std::cout << std::endl;
	std::cout << "      ";
	for (int j=0; j<n; j++) {
		std::cout << "-----";
	}
	std::cout << std::endl;
	for (int i=0; i<n; i++) {
		std::cout << std::setw(5) << format(row_product[i]) << "|";
		for (int j=0; j<n; j++) {
			std::cout << std::setw(5) << format((*grid)[i][j]);
		}
		std::cout << "|" << std::endl;
	}
	std::cout << "      ";
	for (int j=0; j<n; j++) {
		std::cout << "-----";
	}
	std::cout << std::endl;
}

void printSolution() {
	printGrid(&solution);
}

void printBoard() {
	printGrid(&board);
	std::cout << "\033[" << (n+3) << "A";
}

void addToBoard(int i, int j, int value) {
	board[i][j] = value;
}

void removeFromBoard(int i, int j) {
	board[i][j] = 0;
}

void saveSolution() {
	for (int i=0; i<n; ++i) {
		for (int j=0; j<n; j++) {
			solution[i][j] = board[i][j];
		}
	}
}

int getLineProductSum(std::function<int(int)> getElement) {
	int sum = 0;
	int current = 0;
	for (int k = 0; k < n; k++) {
		int value = getElement(k);
		if (value == 0 || value == -1) {
			sum += current;
			current = 0;
		} else {
			if (current == 0) {
				current = 1;
			}
			current *= value;
		}
	}
	sum += current;
	return sum;
}

bool isLinePartiallyOk(int constraint, std::function<int(int)> getElement) {
	if (constraint == 0) {
		return true;
	}
	int product = getLineProductSum(getElement);
	return product <= constraint;
}

bool isRowPartiallyOk(int i) {
	return isLinePartiallyOk(row_product[i], [i](int j) { return board[i][j]; });
}

bool isColPartiallyOk(int j) {
	return isLinePartiallyOk(col_product[j], [j](int i) { return board[i][j]; });
}

bool isLineOk(int constraint, std::function<int(int)> getElement) {
	if (constraint == 0) {
		return true;
	}
	int product = getLineProductSum(getElement);
	return product == constraint;
}

bool isRowOk(int i) {
	return isLineOk(row_product[i], [i](int j) { return board[i][j]; });
}

bool isColOk(int j) {
	return isLineOk(col_product[j], [j](int i) { return board[i][j]; });
}

bool isValid(int i, int j) {
	return 0 <= i && i < n && 0 <= j && j < n;
}

bool isBoardConnected() {
	std::pair<int,int> start = {-1, -1};
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (board[i][j] > 0) {
				start = {i, j};
				break;
			}
		}
		if (start.first != -1) {
			break;
		}
	}
	if (start.first == -1) {
		return true; // Empty board.
	}
	std::queue<std::pair<int,int>> q;
	q.push(start);
	bool seen[n][n] = {0};
	seen[start.first][start.second] = true;
	const std::vector<std::pair<int, int>> directions = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
	while (!q.empty()) {
		auto [i, j] = q.front();
		q.pop();
		for (const auto& [di,dj] : directions) {
			int ni = i + di, nj = j + dj;
			if (!isValid(ni, nj) || seen[ni][nj] || board[ni][nj] == -1) {
				continue;
			}
			seen[ni][nj] = true;
			q.push({ni, nj});
		}
	}

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (board[i][j] > 0 && !seen[i][j]) {
				return false;
			}
		}
	}
	return true;
}

struct RemainingRegion {
	int top, bottom, left, right;
};

struct HookShape {
	int row_i, col_j, i_max, j_max;
	// Hook consists of board[i][col_j] for i <= i_max
	//              and board[row_i][j] for j <= j_max
};

void backtrack(RemainingRegion region, HookShape shape, int i, int j, int hook, int count);

void processCell(int i, int j, int value, int hook, RemainingRegion region,
		HookShape shape, int next_i, int next_j, int count) {
	addToBoard(i, j, value);
	if (isRowPartiallyOk(i) && isColPartiallyOk(j)
			&& !(i == shape.i_max && !isColOk(shape.col_j))
			&& !(j == shape.j_max && !isRowOk(shape.row_i))) {
		backtrack(region, shape, next_i, next_j, hook, count);
	}
	removeFromBoard(i, j);
}

void backtrack(RemainingRegion region = {0, n - 1, 0, n - 1},
			HookShape shape = {-1, -1, -1, -1}, int i = 0, int j = 0,
			int hook = n+1, int count = 0) {
	int top = region.top, bottom = region.bottom, left = region.left, right = region.right;
	int row_i = shape.row_i, col_j = shape.col_j, i_max = shape.i_max, j_max = shape.j_max;

	if (count < 0) {
		return;
	}

	if ((i_max - i + 1) + (j_max - j + 1) < count) {
		return;
	}

	if (i < i_max + 1) {
		processCell(i, col_j, hook, hook, region, shape, i+1, j, count-1);
		processCell(i, col_j, -1,   hook, region, shape, i+1, j, count); // skip cell
	} else if (j < j_max + 1) {
		processCell(row_i, j, hook, hook, region, shape, i, j+1, count-1);
		processCell(row_i, j, -1,   hook, region, shape, i, j+1, count); // skip cell
	} else {
		if (count != 0) {
			return;
		}
		if (!isBoardConnected()) {
			return;
		}
		if (hook == 1) {
			saveSolution();
			printSolution();
			solution_count += 1;
			std::cout << std::endl << std::endl << std::endl;
			return;
		}
		print_count += 1;
		if (print_count == 1e1) {
			printBoard();
			print_count = 0;
		}
		int new_hook = hook-1;
		if (new_hook > 1) {
			backtrack({top+1, bottom, left+1, right}, {top,    left,  bottom, right}, top, left+1, new_hook, new_hook);
			backtrack({top, bottom-1, left+1, right}, {bottom, left,  bottom, right}, top, left+1, new_hook, new_hook);
			backtrack({top+1, bottom, left, right-1}, {top,    right, bottom, right-1}, top, left, new_hook, new_hook);
			backtrack({top, bottom-1, left, right-1}, {bottom, right, bottom, right-1}, top, left, new_hook, new_hook);
		} else {
			backtrack({top+1, bottom, left+1, right}, {top,    left,  bottom, right}, top, left+1, new_hook, new_hook);
		}
	}
}

int dfs(int i, int j, bool (&seen)[n][n]) {
	if (!isValid(i, j) || solution[i][j] != -1 || seen[i][j]) {
		return 0;
	}
	seen[i][j] = true;
	int result = 1;
	const std::vector<std::pair<int, int>> directions = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
	for (const auto& [di, dj] : directions) {
		result += dfs(i + di, j + dj, seen);
	}
	return result;
}

int getProductOfAreasOfConnectedEmptySquares() {
	int product = 1;
	bool seen[n][n] = {0};
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			int area = dfs(i, j, seen);
			if (area > 0) {
				product *= area;
			}
		}
	}
	return product;
}

int main() {
	backtrack();
	printSolution();
	std::cout << "solution_count: " << solution_count << std::endl;
	int seen[n] = {0};
	int answer = 0;
	answer = getProductOfAreasOfConnectedEmptySquares();
	std::cout << "answer: " << answer << std::endl;
}
