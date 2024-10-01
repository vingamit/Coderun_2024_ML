#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>
#include <chrono>
#include <climits>  // Include this header for INT_MAX

int LevDistBounded(const std::string& a, const std::string& b, int k = 2) {
    int n = a.length();
    int m = b.length();

    if (abs(m - n) > k) {
        return k + 1;
    }

    std::vector<int> prev_prev(m + 1, INT_MAX);
    std::vector<int> prev(m + 1);
    std::vector<int> curr(m + 1, INT_MAX);

    for (int j = 0; j <= std::min(m, k); ++j) {
        prev[j] = j;
    }

    for (int i = 0; i < n; ++i) {
        curr[0] = i + 1;

        int stripe_start = std::max(0, i - k);
        int stripe_end = std::min(m, i + k + 1);

        if (stripe_start > 0) {
            curr[stripe_start] = INT_MAX;
        }

        for (int j = stripe_start; j < stripe_end; ++j) {
            int indicator = (a[i] != b[j]);
            curr[j + 1] = std::min({prev[j + 1] + 1, curr[j] + 1, prev[j] + indicator});

            if (i && j && a[i - 1] == b[j] && a[i] == b[j - 1]) {
                curr[j + 1] = std::min(curr[j + 1], prev_prev[j - 1] + 1);
            }
        }

        std::swap(prev_prev, prev);
        std::swap(prev, curr);
    }

    return prev[m];
}

int dau_lev(const std::string& a, const std::string& b) {
    int n = a.length();
    int m = b.length();

    if (abs(n - m) > 2) {
        return 3;
    }

    std::vector<int> prev_prev(m + 1, INT_MAX);
    std::vector<int> prev(m + 1);
    std::vector<int> curr(m + 1);

    for (int j = 0; j <= m; ++j) {
        prev[j] = j;
    }

    for (int i = 0; i < n; ++i) {
        curr[0] = i + 1;
        for (int j = 0; j < m; ++j) {
            int indicator = (a[i] != b[j]);
            curr[j + 1] = std::min({prev[j + 1] + 1, curr[j] + 1, prev[j] + indicator});

            if (i && j && a[i - 1] == b[j] && a[i] == b[j - 1]) {
                curr[j + 1] = std::min(curr[j + 1], prev_prev[j - 1] + 1);
            }
        }

        std::swap(prev_prev, prev);
        std::swap(prev, curr);
    }

    return prev[m];
}

std::vector<std::string> restore(const std::string& a, const std::string& b) {
    int n = a.length();
    int m = b.length();

    std::vector<std::vector<int>> dp(n + 1, std::vector<int>(m + 1));
    std::vector<std::vector<std::tuple<char, int, std::string>>> ops(n + 1, std::vector<std::tuple<char, int, std::string>>(m + 1));

    ops[0][0] = std::make_tuple('M', 0, "");

    for (int i = 1; i <= n; ++i) {
        dp[i][0] = i;
        ops[i][0] = std::make_tuple('D', i - 1, std::string(1, a[i - 1]));
    }
    for (int j = 1; j <= m; ++j) {
        dp[0][j] = j;
        ops[0][j] = std::make_tuple('I', 0, std::string(1, b[j - 1]));
    }

    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            int indicator = (a[i - 1] != b[j - 1]);
            dp[i][j] = std::min({dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + indicator});

            if (dp[i][j] == dp[i - 1][j] + 1) {
                ops[i][j] = std::make_tuple('D', i - 1, "");
            } else if (dp[i][j] == dp[i][j - 1] + 1) {
                ops[i][j] = std::make_tuple('I', i - 1, std::string(1, b[j - 1]));
            } else if (dp[i][j] == dp[i - 1][j - 1] + indicator) {
                if (indicator) {
                    ops[i][j] = std::make_tuple('S', i - 1, std::string(1, b[j - 1]));
                } else {
                    ops[i][j] = std::make_tuple('M', i - 1, std::string(1, a[i - 1]));
                }
            }

            if (i > 1 && j > 1 && a[i - 2] == b[j - 1] && a[i - 1] == b[j - 2]) {
                if (dp[i][j] > dp[i - 2][j - 2] + 1) {
                    dp[i][j] = dp[i - 2][j - 2] + 1;
                    ops[i][j] = std::make_tuple('T', i - 1, b.substr(j - 2, 2));
                }
            }
        }
    }

    int i = n, j = m;
    std::vector<std::tuple<char, int, std::string>> path;

    while (i > 0 || j > 0) {
        auto now = ops[i][j];
        path.push_back(now);
        char action = std::get<0>(now);

        if (action == 'M' || action == 'S') {
            i--;
            j--;
        } else if (action == 'D') {
            i--;
        } else if (action == 'I') {
            j--;
        } else {  // 'T'
            i -= 2;
            j -= 2;
        }
    }

    std::reverse(path.begin(), path.end());

    std::vector<std::string> result;
    std::string snow;

    for (const auto& step : path) {
        char action;
        int ind;
        std::string let;
        std::tie(action, ind, let) = step;

        if (action == 'T') {
            snow += let[0];
            snow += let[1];
            result.push_back(snow + a.substr(ind + 1));
        } else if (action == 'M') {
            snow += let;
        } else if (action == 'S') {
            snow += let;
            result.push_back(snow + a.substr(ind + 1));
        } else if (action == 'D') {
            result.push_back(snow + a.substr(ind + 1));
        } else if (action == 'I') {
            snow += let;
            result.push_back(snow + a.substr(ind));
        }
    }

    return result;
}

std::string process_query(const std::string& s, const std::vector<std::string>& dictionary, const std::vector<int>& le_mas) {
    int n = s.length();
    auto left = std::lower_bound(le_mas.begin(), le_mas.end(), n - 2);
    auto right = std::upper_bound(le_mas.begin(), le_mas.end(), n + 2);

    int bscore = 3;
    std::string bword;

    for (auto it = left; it < right; ++it) {
        std::string word = dictionary[it - le_mas.begin()];
        int kscore = LevDistBounded(s, word);
        if (kscore < 3) {
            int score = dau_lev(s, word);
            if (score == 1) {
                return s + " 1 " + word;
            }
            if (bscore > score) {
                bscore = score;
                bword = word;
            }
        }
    }

    if (bscore < 3) {
        std::string mid = restore(s, bword)[0];
        return s + " 2 " + mid + " " + bword;
    }

    return s + " 3+";
}

int main() {
    std::ifstream dict_file("dict.txt", std::ios::in | std::ios::binary);
    std::vector<std::string> di_list;
    std::string line;

    while (std::getline(dict_file, line)) {
        if (!line.empty() && line.back() == '\n') {
            line.pop_back();
        }
        di_list.push_back(line);
    }
    dict_file.close();

    std::sort(di_list.begin(), di_list.end(), [](const std::string& a, const std::string& b) {
        return a.length() < b.length();
    });

    std::vector<int> le_mas;
    for (const auto& word : di_list) {
        le_mas.push_back(word.length());
    }
    std::set<std::string> di_set(di_list.begin(), di_list.end());

    std::ifstream query_file("queries.txt", std::ios::in | std::ios::binary);
    std::vector<std::string> queries;

    while (std::getline(query_file, line)) {
        if (!line.empty() && line.back() == '\n') {
            line.pop_back();
        }
        queries.push_back(line);
    }
    query_file.close();

    std::vector<std::string> res;
    int i = 0;
    auto start = std::chrono::steady_clock::now();

    for (const auto& query : queries) {
        i++;
        if (di_set.find(query) != di_set.end()) {
            res.push_back(query + " 0");
        } else {
            std::string row = process_query(query, di_list, le_mas);
            res.push_back(row);
        }

        if (i % 100 == 0) {
            auto now = std::chrono::steady_clock::now();
            std::chrono::duration<double> elapsed = now - start;
            std::cout << i << " " << elapsed.count() << std::endl;
            std::cout << res.back() << std::endl;
        }
    }

    std::ofstream answer_file("answer1.txt", std::ios::out | std::ios::binary);
    for (const auto& r : res) {
        answer_file << r << "\n";
    }
    answer_file.close();

    return 0;
}
