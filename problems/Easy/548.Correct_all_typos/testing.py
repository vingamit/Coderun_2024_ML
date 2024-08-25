def levenshtein_distance(s1, s2):
    len_s1 = len(s1)
    len_s2 = len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]
    operations = [[None] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        dp[i][0] = i
        operations[i][0] = ('delete', i - 1)
    for j in range(len_s2 + 1):
        dp[0][j] = j
        operations[0][j] = ('insert', j - 1)

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
                operations[i][j] = ('none',)
            else:
                delete = dp[i - 1][j] + 1
                insert = dp[i][j - 1] + 1
                substitute = dp[i - 1][j - 1] + 1
                dp[i][j] = min(delete, insert, substitute)
                if dp[i][j] == delete:
                    operations[i][j] = ('delete', i - 1)
                elif dp[i][j] == insert:
                    operations[i][j] = ('insert', j - 1)
                else:
                    operations[i][j] = ('substitute', i - 1, j - 1)
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                transpose = dp[i - 2][j - 2] + 1
                if dp[i][j] > transpose:
                    dp[i][j] = transpose
                    operations[i][j] = ('transpose', i - 2, j - 2)

    return dp, operations

def reconstruct_path(s1, s2, dp, operations):
    i, j = len(s1), len(s2)
    path = [s1]
    while i > 0 and j > 0:
        op = operations[i][j]
        if op[0] == 'none':
            i -= 1
            j -= 1
        elif op[0] == 'delete':
            i -= 1
            return s1[:i] + s1[i + 1:]
        elif op[0] == 'insert':
            j -= 1
            return s1[:i] + s2[j] + s1[i:]
        elif op[0] == 'substitute':
            i -= 1
            j -= 1
            return s1[:i] + s2[j] + s1[i + 1:]
        elif op[0] == 'transpose':
            i -= 2
            j -= 2
            return s1[:i] + s1[i + 1] + s1[i] + s1[i + 2:]
    while i > 0:
        i -= 1
        return s1[:i] + s1[i + 1:]
    while j > 0:
        j -= 1
        return s1[:i] + s2[j] + s1[i:]

def func(s1, s2):
    dp, operations = levenshtein_distance(s1, s2)
    path = reconstruct_path(s1, s2, dp, operations)
    return path
