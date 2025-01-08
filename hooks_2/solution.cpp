#include <iostream>
#include <iomanip>

const int n = 9;
int row_sum[n] = {45, 44, 4, 48, 7, 14, 47, 43, 33};
int col_sum[n] = {36, 5, 47, 35, 17, 30, 21, 49, 45};
// const int n = 4;
// int row_sum[n] = {7, 11, 4, 8};
// int col_sum[n] = {10, 3, 5, 12};

int board[n][n];
int solution[n][n];

int solution_count = 0;
int print_count = 0;

void printGrid(int (*grid)[n][n]) {
	std::cout << "    ";
	for (int j=0; j<n; j++) {
		std::cout << std::setw(3) << col_sum[j] << " ";
	}
	std::cout << std::endl;
	for (int i=0; i<n; i++) {
		std::cout << std::setw(3) << row_sum[i];
		for (int j=0; j<n; j++) {
			std::string b = (*grid)[i][j] == 0 ? "" : std::to_string((*grid)[i][j]);
			std::cout << std::setw(3) << b << " ";
		}
		std::cout << std::endl;
	}
	std::cout << std::endl;
}

void printSolution() {
	printGrid(&solution);
}

void printBoard() {
	printGrid(&board);
	std::cout << "\033[" << (n+2) << "A";
}

void addToBoard(int i, int j, int value) {
	board[i][j] = value;
	row_sum[i] -= value;
	col_sum[j] -= value;
}

void removeFromBoard(int i, int j) {
	int value = board[i][j];
	board[i][j] = 0;
	row_sum[i] += value;
	col_sum[j] += value;
}

void saveSolution() {
	for (int i=0; i<n; ++i) {
		for (int j=0; j<n; j++) {
			solution[i][j] = board[i][j];
		}
	}
}

void backtrack(int top = 0, int bottom = n - 1, int left = 0, int right = n - 1,
			int row_i = -1, int col_j = -1, int i_min = -1, int i_max = -1, int j_min = -1, int j_max = -1,
			int hook = n+1, int count = 0) {
	if (count == 0) {
		if (hook == 1) {
			saveSolution();
			solution_count += 1;
			return;
		}
		print_count += 1;
		if (print_count == 1e3) {
			printBoard();
			print_count = 0;
		}
		int new_hook = hook-1;
		if (new_hook > 1) {
			backtrack(top+1, bottom, left+1, right,  top, left,      top, bottom, left+1, right, new_hook, new_hook);
			backtrack(top, bottom-1, left+1, right,  bottom, left,   top, bottom, left+1, right, new_hook, new_hook);
			backtrack(top+1, bottom, left, right-1,  top, right,     top, bottom, left, right-1, new_hook, new_hook);
			backtrack(top, bottom-1, left, right-1,  bottom, right,  top, bottom, left, right-1, new_hook, new_hook);
		} else {
			backtrack(top+1, bottom, left+1, right,  top, left,      top, bottom, left+1, right, new_hook, new_hook);
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

	for (int i = i_min; i < i_max + 1; ++i) {
		addToBoard(i, col_j, hook);
		if ((row_sum[i] >= 0 && col_sum[col_j] >= 0) && !(i == i_max && col_sum[col_j] != 0)) {
			backtrack(top, bottom, left, right, row_i, col_j, i + 1, i_max, j_min, j_max, hook, count - 1);
		}
		removeFromBoard(i, col_j);
	}

	for (int j = j_min; j < j_max + 1; j++) {
		addToBoard(row_i, j, hook);
		if ((row_sum[row_i] >= 0 && col_sum[j] >= 0) && !(j == j_max && row_sum[row_i] != 0)) {
			backtrack(top, bottom, left, right, row_i, col_j, i_max + 1, i_max, j + 1, j_max, hook, count - 1);
		}
		removeFromBoard(row_i, j);
	}
}

void getLargestProduct(int j, int *seen, int current, int &answer) {
	if (j == n) {
		answer = std::max(answer, current);
		return;
	}
	if (current == 0) {
		return;
	}
	for (int i = 0; i < n; i++) {
		if (seen[i]) {
			continue;
		}
		seen[i] = true;
		getLargestProduct(j+1, seen, current * solution[i][j], answer);
		seen[i] = false;
	}
}

int main() {
	backtrack();
	printSolution();
	std::cout << "solution_count: " << solution_count << std::endl;
	int seen[n] = {0};
	int answer = 0;
	getLargestProduct(0, seen, 1, answer);
	std::cout << "answer: " << answer << std::endl;
}
