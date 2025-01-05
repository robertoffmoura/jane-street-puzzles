#include <iostream>
#include <vector>
#include <unordered_set>

const int n = 100;

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

void recurse(int i, int& print_count) {
	if (seen.find(i) != seen.end()) {
		return;
	}
	seen.insert(i);
	current.push_back(i);

	if (print_count == 100000) {
		delete_last_lines(2);
		for (int k : current) {
			std::cout << k << " ";
		}
		std::cout << std::endl;
		for (int k : best) {
			std::cout << k << " ";
		}
		std::cout << std::endl;
		print_count = 0;
	}
	++print_count;

	if (current.size() > best.size()) {
		best = current;
	}
	for (int j : neighbors[i]) {
		recurse(j, print_count);
	}
	current.pop_back();
	seen.erase(i);
}

std::vector<int> solve() {
	int print_count = 0;
	for (int i = 1; i <= n; ++i) {
		std::cout << "i is " << i << std::endl;
		recurse(i, print_count);
	}
	return best;
}

int main() {
	for (int i = 1; i <= n; ++i) {
		for (int j = 1; j <= n; ++j) {
			if (i == j || i % j != 0) {
				continue;
			}
			neighbors[i].push_back(j);
			neighbors[j].push_back(i);
		}
	}

	std::cout << "\n\n";
	std::vector<int> result = solve();
	for (int i = 0; i < result.size(); ++i) {
		std::cout << result[i] << " ";
	}
	std::cout << std::endl;

	return 0;
}
