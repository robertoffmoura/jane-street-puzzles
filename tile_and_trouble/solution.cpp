#include <iomanip>
#include <iostream>
#include <vector>

int n = 12;
std::vector<std::vector<int>> board(n, std::vector<int>(n, -1));
std::vector<int> row_sum = {12, 17, 43, 44, 34, 42, 43, 21, 36, 29, 30, 26};
std::vector<int> col_sum = {30, 35, 45, 43, 41, 28, 25, 29, 25, 38, 18, 20};
int max_tile = 5;

bool canPlace(int d, int i, int j) {
	if (i + d > n || j + d > n)
		return false;
	for (int di = 0; di < d; ++di) {
		for (int dj = 0; dj < d; ++dj) {
			if (board[i + di][j + dj] != -1)
				return false;
		}
	}
	for (int di = 0; di < d; ++di) {
		if (row_sum[i + di] - d * d < 0)
			return false;
	}
	for (int dj = 0; dj < d; ++dj) {
		if (col_sum[j + dj] - d * d < 0)
			return false;
	}
	return true;
}

void addToBoard(int d, int i, int j) {
	for (int di = 0; di < d; ++di) {
		for (int dj = 0; dj < d; ++dj) {
			board[i + di][j + dj] = d;
		}
	}
	for (int di = 0; di < d; ++di) {
		row_sum[i + di] -= d * d;
	}
	for (int dj = 0; dj < d; ++dj) {
		col_sum[j + dj] -= d * d;
	}
}

void removeFromBoard(int d, int i, int j) {
	for (int di = 0; di < d; ++di) {
		for (int dj = 0; dj < d; ++dj) {
			board[i + di][j + dj] = -1;
		}
	}
	for (int di = 0; di < d; ++di) {
		row_sum[i + di] += d * d;
	}
	for (int dj = 0; dj < d; ++dj) {
		col_sum[j + dj] += d * d;
	}
}

void printBoard() {
	for (int j = 0; j < n; ++j) {
		std::cout << "---";
	}
	std::cout << std::endl;
	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < n; ++j) {
			std::cout << std::setw(2) << std::right << board[i][j] << " ";
		}
		std::cout << "| " << std::setw(2) << std::right << row_sum[i] << std::endl;
	}
	for (int j = 0; j < n; ++j) {
		std::cout << "---";
	}
	std::cout << std::endl;
	for (int j = 0; j < n; ++j) {
		std::cout << std::setw(2) << std::right << col_sum[j] << " ";
	}
	std::cout << std::endl;
}

void recurse(int idx, bool& found_solution, int& print_count) {
	if (found_solution)
		return;

	if (print_count == 1000000) {
		print_count = 0;
		printBoard();
		std::cout << "\033[" << n + 3 << "A\033[K";
	}
	print_count++;

	if (idx > 0) {
		int i = (idx - 1) / n;
		int j = (idx - 1) % n;
		if (j == n - 1 && row_sum[i] != 0)
			return;
		if (i == n - 1 && col_sum[j] != 0)
			return;
	}

	if (idx == n * n - 1) {
		std::cout << "SOLUTION!!!" << std::endl;
		printBoard();
		found_solution = true;
		return;
	}

	int i = idx / n;
	int j = idx % n;

	if (board[i][j] != -1) {
		recurse(idx + 1, found_solution, print_count);
		return;
	}

	board[i][j] = 0;
	recurse(idx + 1, found_solution, print_count);
	board[i][j] = -1;

	for (int d = 1; d <= max_tile; ++d) {
		if (!canPlace(d, i, j))
			break;
		addToBoard(d, i, j);
		recurse(idx + d, found_solution, print_count);
		removeFromBoard(d, i, j);
	}
}

int main() {
	bool found_solution = false;
	int print_count = 0;
	recurse(0, found_solution, print_count);
	return 0;
}
