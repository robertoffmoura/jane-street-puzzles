#include <iostream>
#include <vector>
#include <unordered_set>
#include <stdlib.h>

const int n = 100;
const int iterations = 1e6;

std::vector<int> neighbors[n + 1];

void delete_last_lines(int n) {
	// Move the cursor to the start of the last line to be deleted
	std::cout << "\x1b[" << n << "F";
	// Clear each of the last n lines
	for (int i = 0; i < n; ++i) {
		std::cout << "\x1b[2K";
	}
	// Move the cursor back to the beginning of the line
	std::cout << "\r" << std::flush;
}

std::vector<int> best;
std::vector<int> current;
std::unordered_set<int> seen;

void print_vector(std::vector<int>& v) {
	for (int k : v) {
		std::cout << k << " ";
	}
	std::cout << std::endl;
}

std::vector<int> get_valid_neighbors(int i) {
	std::vector<int> result;
	for (int j : neighbors[i]) {
		if (seen.find(j) != seen.end()) {
			continue;
		}
		result.push_back(j);
	}
	return result;
}

void recurse(int i, int& print_count) {
	seen.insert(i);
	current.push_back(i);

	if (print_count == 100000) {
		delete_last_lines(3);
		print_vector(current);
		print_vector(best);
		std::cout << "best length: " << best.size() << std::endl;;
		print_count = 0;
	}
	++print_count;

	if (current.size() > best.size()) {
		best = current;
	}
	std::vector<int> valid_neighbors = get_valid_neighbors(i);
	int size = valid_neighbors.size();
	if (size > 0) {
		int index = rand() % size;
		recurse(valid_neighbors[index], print_count);
	}
	current.pop_back();
	seen.erase(i);
}

std::vector<int> solve() {
	int print_count = 0;
	for (int i = 1; i < iterations; ++i) {
		recurse(rand() % (n+1), print_count);
	}
	return best;
}

int main() {
	for (int i = 1; i <= n; ++i) {
		for (int j = i+1; j <= n; ++j) {
			if (j % i != 0) {
				continue;
			}
			neighbors[i].push_back(j);
			neighbors[j].push_back(i);
		}
	}

	std::cout << "\n\n";
	std::vector<int> result = solve();
	print_vector(result);

	return 0;
}
