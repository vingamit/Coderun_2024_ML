import re
from typing import List, Tuple
import time

def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i-1, j)] + 1,  # deletion
                d[(i, j-1)] + 1,  # insertion
                d[(i-1, j-1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j-1] and s1[i-1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i-2, j-2)] + 1)  # transposition
    return d[lenstr1-1, lenstr2-1]

def get_corrections(word: str, dictionary: List[str]) -> Tuple[int, List[str]]:
    min_distance = float('inf')
    corrections = []
    
    for dict_word in dictionary:
        distance = damerau_levenshtein_distance(word, dict_word)
        if distance < min_distance:
            min_distance = distance
            corrections = [dict_word]
        elif distance == min_distance:
            corrections.append(dict_word)
    
    return min_distance, corrections

def get_step_by_step_correction(word: str, correction: str) -> List[str]:
    steps = []
    i, j = 0, 0
    
    while i < len(word) and j < len(correction):
        if word[i] != correction[j]:
            if i < len(word) - 1 and j < len(correction) - 1 and word[i] == correction[j+1] and word[i+1] == correction[j]:
                # Transposition
                steps.append(word[:i] + word[i+1] + word[i] + word[i+2:])
                i += 2
                j += 2
            elif len(word) > len(correction):  # deletion
                steps.append(word[:i] + word[i+1:])
                i += 1
            elif len(word) < len(correction):  # insertion
                steps.append(word[:i] + correction[j] + word[i:])
                j += 1
            else:  # substitution
                steps.append(word[:i] + correction[j] + word[i+1:])
                i += 1
                j += 1
        else:
            i += 1
            j += 1
    
    # Handle remaining characters
    if i < len(word):
        steps.append(word[:i])
    elif j < len(correction):
        steps.append(word + correction[j:])
    
    return steps

def process_query(query: str, dictionary: List[str]) -> str:
    distance, corrections = get_corrections(query, dictionary)
    
    if distance == 0:
        return f"{query} 0"
    elif distance == 1:
        return f"{query} 1 {corrections[0]}"
    elif distance == 2:
        steps = get_step_by_step_correction(query, corrections[0])
        return f"{query} 2 {steps[0]} {corrections[0]}"
    else:
        return f"{query} 3+"

# Read dictionary
with open('dict.txt', 'r', encoding='utf-8') as f:
    dictionary = [line.strip() for line in f]

with open('queries.txt', 'r', encoding='utf-8') as f:
    querys = [line.strip() for line in f]

# Process queries and write results
with open('answer.txt', 'w', encoding='utf-8') as answer_file:
    for query in querys:
        start = time.time()
        result = process_query(query, dictionary)
        print(result)
        print(time.time() - start)
        answer_file.write(result + '\n')