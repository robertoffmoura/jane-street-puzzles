#include <utility>
#include <vector>
#include <iostream>

/*
1
2  3
4  5  6
7  8  9  10
11 12 13 14 15
*/

int n = 5;
int paired[5][5] = {0};
int paired_count = 0;

int is_valid(int i, int j) {
	return 0 <= i && i < n && 0 <= j && j <= i;
}

std::vector<std::pair<int,int>> get_neighbors(int i, int j) {
	return {{i+1,j}, {i+1,j+1}, {i,j+1}};
}

int result = 0;

void recurse(int i, int j) {
	if (i == n) {
		if (paired_count == 7) {
			result += 1;
		}
		return;
	}
	if (j > i) {
		recurse(i+1, 0);
		return;
	}
	recurse(i, j+1);
	if (!paired[i][j]) {
		for (const auto& [ni, nj] : get_neighbors(i, j)) {
			if (!is_valid(ni,nj) || paired[ni][nj]) {
				continue;
			}
			paired[i][j] = paired[ni][nj] = true;
			paired_count++;
			recurse(i, j+1);
			paired_count--;
			paired[i][j] = paired[ni][nj] = false;
		}
	}
}

int main() {
	recurse(0,0);
	std::cout << result << std::endl;
}
