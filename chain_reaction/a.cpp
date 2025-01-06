#include <iostream>
#include <unordered_set>
#include <random>

const int n = 100;
const int iterations = 1e8;
const int max_neighbors = 100;

int neighbors[n + 1][max_neighbors];
int neighbor_count[n + 1] = {0};

int best[n + 1] = {0};
int best_size = 0;

int current[n + 1] = {0};
int current_size = 0;

std::unordered_set<int> seen;
std::mt19937 rng(std::random_device{}());

inline void print_array(const int* arr, int size) {
	for (int i = 0; i < size; ++i) {
		std::cout << arr[i] << " ";
	}
	std::cout << "\n";
}

inline int get_valid_neighbors(int i, int* result) {
	int count = 0;
	for (int j = 0; j < neighbor_count[i]; ++j) {
		int neighbor = neighbors[i][j];
		if (seen.count(neighbor) == 0) {
			result[count++] = neighbor;
		}
	}
	return count;
}

void recurse(int i, int& print_count) {
	seen.insert(i);
	current[current_size++] = i;

	if (++print_count == 100000) {
		print_count = 0;
		std::cout << "\x1b[3F\x1b[2K";
		print_array(current, current_size);
		print_array(best, best_size);
		std::cout << "best length: " << best_size << "\n";
	}

	if (current_size > best_size) {
		best_size = current_size;
		std::copy(current, current + current_size, best);
	}

	int valid_neighbors[max_neighbors];
	int valid_count = get_valid_neighbors(i, valid_neighbors);

	if (current_size > 40) {
		for (int j = 0; j < valid_count; ++j) {
			recurse(valid_neighbors[j], print_count);
		}
	} else {
		if (valid_count > 0) {
			std::uniform_int_distribution<int> dist(0, valid_count - 1);
			recurse(valid_neighbors[dist(rng)], print_count);
		}
	}

	--current_size;
	seen.erase(i);
}

void solve() {
	int print_count = 0;
	for (int i = 0; i < iterations; ++i) {
		recurse(rng() % (n + 1), print_count);
	}
}

int main() {
	for (int i = 1; i <= n; ++i) {
		for (int j = i + i; j <= n; j += i) {
			neighbors[i][neighbor_count[i]++] = j;
			neighbors[j][neighbor_count[j]++] = i;
		}
	}

	std::cout << "\n\n";
	solve();
	print_array(best, best_size);

	return 0;
}
