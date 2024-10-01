from typing import Set, List, Tuple

def dau_lev(s1: str, s2: str) -> int:
    n, m = len(s1), len(s2)

    if abs(n - m) > 2:
        return 3
    
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][0] = i
    for j in range(1, m + 1):
        dp[0][j] = j
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = s1[i - 1] != s2[j - 1]

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

            if i > 1 and j > 1 and s1[i - 2] == s2[j - 1] and s1[i - 1] == s2[j - 2]:
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)

    return dp[n][m]

def calc_path_for_2(s1: str, s2: str) -> str:
    n, m = len(s1), len(s2)
    
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    ops = [[None for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][0] = i
        ops[i][0] = ("D", i - 1, s1[i - 1])
    for j in range(1, m + 1):
        dp[0][j] = j
        ops[0][j] = ("I", j - 1, s2[j - 1])
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = s1[i - 1] != s2[j - 1]

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )
            if dp[i][j] == dp[i - 1][j] + 1:
                ops[i][j] = ("D", i - 1, "")
            elif dp[i][j] == dp[i][j - 1] + 1:
                ops[i][j] = ("I", j - 1, s2[j - 1])
            else:
                ops[i][j] = ("S" if cost else "M", i - 1, s2[j - 1])

            if i > 1 and j > 1 and s1[i - 2] == s2[j - 1] and s1[i - 1] == s2[j - 2]:
                if dp[i][j] > dp[i - 2][j - 2] + 1:
                    dp[i][j] = dp[i - 2][j - 2] + 1
                    ops[i][j] = ("T", i - 2, s1[i - 1] + s1[i - 2])

    i, j = n, m
    last = None
    while i > 0 or j > 0:
        now = ops[i][j]
        if now[0] == "M":
            i -= 1
            j -= 1
        elif now[0] == "S":
            i -= 1
            j -= 1
            first = s1[:now[1]] + now[2] + s1[now[1] + 1:]
        elif now[0] == "D":
            i -= 1
            first = s1[:now[1]] + s1[now[1] + 1:]
        elif now[0] == "I":
            j -= 1
            first = s1[:now[1]] + now[2] + s1[now[1]:]
        elif now[0] == "T":
            i -= 2
            j -= 2
            first = s1[:now[1]] + now[2] + s1[now[1] + 2:]
    return first



def check(word: str, dictionary: Set[str]) -> str:
    if word in dictionary:
        return f"{word} 0"
    
    for dword in dictionary:
        score = dau_lev(word, dword)
        if score == 1:
            return f"{word} 1 {dword}"
        elif score == 2:
            mid = calc_path_for_2(word, dword)
            return f"{word} 2 {mid} {dword}"

    return f"{word} 3+"

def main():
    with open("dict.txt", "r") as file:
        dictionary = set(line.rstrip() for line in file)
    
    with open("queries.txt", "r") as file:
        queries = [line.rstrip() for line in file]
    
    for query in queries:
        print(check(query, dictionary))
    
if __name__ == "__main__":
    main()
