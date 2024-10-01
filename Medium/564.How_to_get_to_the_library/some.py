import sys
from collections import defaultdict
import random
import time
import heapq

def levenshtein_distance(s1, s2):
    """Функция для расчета расстояния Левенштейна"""
    n, m = len(s1), len(s2)
    if n > m:
        s1, s2 = s2, s1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous_row[j] + 1, current_row[j - 1] + 1
            change = previous_row[j - 1] + (s1[j - 1] != s2[i - 1])
            current_row[j] = min(add, delete, change)
    
    return current_row[n]

def preprocess_library(books, inter=(3, 3)):
    ngram_index = defaultdict(set)
    for n in range(inter[0], inter[1] + 1):
        for book in books:
            ngrams = create_ngrams(book.lower(), n)
            for ngram in ngrams:
                ngram_index[ngram].add(book)
    
    return ngram_index

def create_ngrams(title, n=3):
    return [title[i:i+n] for i in range(len(title) - n + 1)]

def load_books():
    with open('htgtl_books.txt', 'r') as file:
        books = [line.strip() for line in file]
    return books

def load_quer_and_ans():
    with open('htgtl_simple_public_queries.txt', 'r') as file:
        lines = [line.strip() for line in file]
        queries = lines[::2]
        answers = lines[1::2]
    return queries, answers

def find_closest_books(query, ngram_index, books, inter=(3, 3), max_results=3):
    query_ngrams = set()
    for n in range(inter[0], inter[1] + 1):
        query_ngrams.update(set(create_ngrams(query.lower(), n)))

    books_scores = defaultdict(int)
    for ngram in query_ngrams:
        for book in ngram_index.get(ngram, []):
            books_scores[book] += 1
    
    top_books_heap = []
    for book, score in books_scores.items():
        if len(top_books_heap) < 40:
            heapq.heappush(top_books_heap, (score, book))
        elif score > top_books_heap[0][0]:
            heapq.heappop(top_books_heap)
            heapq.heappush(top_books_heap, (score, book))
    
    results = []
    for _, book in top_books_heap:
        distance = levenshtein_distance(query.lower(), book.lower())
        results.append((book, distance))
    
    return [book for book, _ in sorted(results, key=lambda x: x[1])[:max_results]]

def main():
    n = int(sys.stdin.readline().strip())
    books = [sys.stdin.readline().rstrip() for _ in range(n)]
    m = int(sys.stdin.readline().strip())
    queries = [sys.stdin.readline().rstrip() for _ in range(m)]
    # books = load_books()
    # queries, answers = load_quer_and_ans()
    # queries, answers = queries[:500], answers[:500]
    
    inter=(3, 4)
    start = time.time()
    ngram_index = preprocess_library(books, inter)
    # print(time.time() - start)
    
    result = []
    for query in queries:
        closest_books = find_closest_books(query, ngram_index, books, inter)
        if len(closest_books) == 0:
            result.append((3, random.choices(books, k=3)))
        else:
            result.append((len(closest_books), closest_books))
    
    for le, col in result:
        print(le)
        print('\n'.join(col))
    # cnt = 0
    # for ans, res in zip(answers, result):
    #     if ans in res[1]:
    #         cnt += 1
    # print(cnt / len(answers), time.time() - start)
    # print(time.time() - start)
    # zero = sum(num == 0 for num, mas in result)
    # print(zero)


if __name__ == "__main__":
    main()