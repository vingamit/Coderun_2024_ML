
import time
from bisect import bisect_left, bisect_right


def LevDistBounded(a, b, k=4):
    n = len(a)
    m = len(b)

    if abs(m - n) > k:
        return k + 1
    
    
    fill_bound = min(m, k)
    prev_prev = [float('inf')] * (m + 1)
    prev = list(range(fill_bound + 1)) + [float('inf')] * (m - fill_bound)
    curr = [float('inf')] * (m + 1)

    for i in range(n):
        curr[0] = i + 1

        # compute stripe indices
        stripe_start = max(0, i - k)
        stripe_end = min(m, i + k + 1)

        # ignore entry left of leftmost
        if stripe_start > 0:
            curr[stripe_start] = float('inf')

        # loop through stripe
        for j in range(stripe_start, stripe_end):
            indicator = a[i] != b[j]
            curr[j + 1] = min(
                prev[j + 1] + 1,
                curr[j] + 1,
                prev[j] + 2 * indicator
            )

            if i and j and a[i - 1] == b[j] and a[i] == b[j - 1]:
                curr[j + 1] = min(curr[j + 1], prev_prev[j - 1] + 1)
        
        prev_prev, prev, curr = prev, curr, prev_prev
    
    return prev[m]

def dau_lev(a, b):
    n, m = len(a), len(b)

    if abs(n - m) > 4:
        return 5

    
    prev_prev = [float('inf')] * (m + 1)
    prev = list(range(m + 1))
    curr = [0] * (m + 1)

    for i in range(n):
        curr[0] = i + 1
        for j in range(m):
            indicator = a[i] != b[j]
            indicator *= 2
            curr[j + 1] = min(
                prev[j + 1] + 1,
                curr[j] + 1,
                prev[j] + indicator
            )

            if i and j and a[i - 1] == b[j] and a[i] == b[j - 1]:
                curr[j + 1] = min(curr[j + 1], prev_prev[j - 1] + 1)
        
        prev_prev, prev, curr = prev, curr, prev_prev
    
    return prev[m]


def restore(a, b):
    n, m = len(a), len(b)

    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    ops = [[None for _ in range(m + 1)] for _ in range(n + 1)]
    ops[0][0] = ("M", 0, "")

    for i in range(1, n + 1):
        dp[i][0] = i
        ops[i][0] = ("D", i - 1, a[i - 1])
    for j in range(1, m + 1):
        dp[0][j] = j
        ops[0][j] = ("I", -1, b[j - 1])
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            indicator = a[i - 1] != b[j - 1]
            indicator *= 2
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + indicator
            )
            if dp[i][j] == dp[i - 1][j] + 1:
                ops[i][j] = ("D", i - 1, "")
            elif dp[i][j] == dp[i][j - 1] + 1:
                ops[i][j] = ("I", i - 1, b[j - 1])
            elif dp[i][j] == dp[i - 1][j - 1] + indicator:
                if indicator:
                    ops[i][j] = ("S", i - 1, b[j - 1])
                else:
                    ops[i][j] = ("M", i - 1, a[i - 1])

            if i > 1 and j > 1 and a[i - 2] == b[j - 1] and a[i - 1] == b[j - 2]:
                if dp[i][j] > dp[i - 2][j - 2] + 1:
                    dp[i][j] = dp[i - 2][j - 2] + 1
                    ops[i][j] = ("T", i - 1, b[j -2:j])
    
    i, j = n, m
    path = []
    while i > 0 or j > 0:
        now = ops[i][j]
        path.append(now)
        if now[0] in ("M", "S"):
            i -= 1
            j -= 1
        elif now[0] == "D":
            i -= 1
        elif now[0] == "I":
            j -= 1
        else:
            i -= 2
            j -= 2
    
    path.reverse()

    snow = []
    res = []
    for action, ind, let in path:
        if action == "T":
            snow.append(let[0])
            snow.append(let[1])
            res.append(''.join(snow) + a[ind + 1:])
        if action == "M":
            snow.append(let)
        if action == "S":
            res.append("".join(snow) + a[ind + 1:])
            snow.append(let)
            res.append("".join(snow) + a[ind + 1:])
        if action == "D":
            res.append("".join(snow) + a[ind + 1:])
        if action == "I":
            snow.append(let)
            res.append("".join(snow) + a[ind + 1:])
    return res

def process_query(s, dictionary, le_mas):
    n = len(s)
    left, right = bisect_left(le_mas, n - 4), bisect_right(le_mas, n + 4)

    bscore = 5
    bword = ""

    for i in range(left, right):
        word = dictionary[i]
        kscore = LevDistBounded(s, word)
        if kscore < 5:
            score = dau_lev(s, word)
            if score == 1:
                return s + " 1 " + word
            if bscore > score:
                bscore = score
                bword = word
    
    if bscore < 5:
        res = restore(s, bword)
        return s + " " + str(len(res)) + " " + ' '.join(res)

    return s + " 5+"


def main():
    j = 20
    with open('dict.txt', 'r') as file:
        di_list= [line.strip() for line in file]
        di_list.sort(key=lambda x: len(x))
        le_mas = [len(word) for word in di_list]
        di_set = set(di_list)
    
    with open('queries.txt', 'r') as file:
        queries = [line.strip() for line in file]
        queries = queries[j * 3334: (j + 1) * 3334]
    
    res = []
    i = 0
    start = time.time()
    for query in queries:
        i += 1
        if query in di_set:
            res.append(query + " 0")
        else:
            row = process_query(query, di_list, le_mas)
            res.append(row)
        
        if i % 100 == 0:
            print(i, time.time() - start)
            print(res[-1])
    
    with open(f"answer" + str(j) + ".txt", 'w') as file:
        file.write('\n'.join(res))


if __name__ == "__main__":
    main()

