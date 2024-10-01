from typing import List, Tuple, Set
from concurrent.futures import ProcessPoolExecutor, as_completed


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    len_s1 = len(s1)
    len_s2 = len(s2)

    if abs(len_s1 - len_s2) > 2:
        return 3
    
    # Инициализация матрицы (размер (len_s1 + 1) x (len_s2 + 1))
    d = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]
    
    # Заполнение первых строк и столбцов
    for i in range(1, len_s1 + 1):
        d[i][0] = i
    for j in range(1, len_s2 + 1):
        d[0][j] = j
    
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            
            d[i][j] = min(
                d[i - 1][j] + 1,     # Удаление
                d[i][j - 1] + 1,     # Вставка
                d[i - 1][j - 1] + cost  # Замена
            )
            
            # Проверка на транспозицию
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    
    return d[len_s1][len_s2]


def get_correction(word: str, dictionary: Set) -> Tuple[int, str]:
    if word in dictionary:
        return 0, ""
    
    for dword in dictionary:
        score = damerau_levenshtein_distance(word, dword)
        if score < 3:
            return score, dword
    
    return 3, ""


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

def get_step_by_step_correction(s1, s2):
    dp, operations = levenshtein_distance(s1, s2)
    preend = reconstruct_path(s1, s2, dp, operations)
    return preend


def process_query(query: str, dictionary: Set) -> str:
    score, word = get_correction(query, dictionary)

    if score == 0:
        return f"{query} 0"
    elif score == 1:
        return f"{query} 1 {word}"
    elif score == 2:
        intermediate = get_step_by_step_correction(query, word)
        return f"{query} 2 {intermediate} {word}"
    else:
        return f"{query} 3+"


def main():
    res = []

    with open('dict.txt', 'r') as file:
        dictionary = set([line.rstrip() for line in file])
    
    with open('queries.txt', 'r') as file:
        querys = [line.rstrip() for line in file]
    
    with ProcessPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_query, query, dictionary) for query in querys]
        
        i = 0
        for future in as_completed(futures):
            i += 1
            if i % 1000 == 0:
                print(i)

        for future in futures:
            res.append(future.result())
    
    with open('answer.txt', 'w', encoding="utf-8") as file:
        file.write('\n'.join(res))


if __name__ == "__main__":
    main()
