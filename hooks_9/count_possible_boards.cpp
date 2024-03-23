#include <iostream>
#include <vector>
#include <unordered_set>

std::vector<std::vector<int>> potential_boards;
int n = 9;
std::vector<int> current;
std::unordered_set<int> seen_hooks;

void get_potential_boards(int k = 0, int top = 0, int bottom = 0, int left = 0, int right = 0) {
    if (k == n - 1) {
        potential_boards.push_back(current);
        return;
    }
    for (int h = 1; h <= n; h++) {
        if (seen_hooks.count(h) > 0) {
            continue;
        }
        if (bottom - top + right - left + 1 < h) {
            continue;
        }
        seen_hooks.insert(h);
        current.push_back(h);
        if (top > 0 && left > 0) {
            get_potential_boards(k + 1, top - 1, bottom, left - 1, right);
        }
        if (top > 0 && right < n - 1) {
            get_potential_boards(k + 1, top - 1, bottom, left, right + 1);
        }
        if (bottom < n - 1 && left > 0) {
            get_potential_boards(k + 1, top, bottom + 1, left - 1, right);
        }
        if (bottom < n - 1 && right < n - 1) {
            get_potential_boards(k + 1, top, bottom + 1, left, right + 1);
        }
        current.pop_back();
        seen_hooks.erase(h);
    }
}

int main() {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            get_potential_boards(0, i, i, j, j);
        }
    }
    std::cout << potential_boards.size() << std::endl;

    return 0;
}