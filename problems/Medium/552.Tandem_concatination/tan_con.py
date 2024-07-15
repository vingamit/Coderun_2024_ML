from typing import List, Tuple
from collections import defaultdict


def is_tandem(row: str) -> bool:
    n = len(row)
    if n % 2 == 1:
        return False
    half = n // 2
    for i in range(half):
        if row[i] != row[half + i]:
            return False
    return True


def calc_pairs(str_seq: List[str]) -> List[Tuple[int, int]]:
    res = set()

    count = defaultdict(set)
    for i, word in enumerate(str_seq):
        count[word].add(i + 1)
    
    for i, word in enumerate(str_seq):
        left, right = [], []
        n = len(word)
        half = len(word) // 2

        for j in range(half + 1):
            part = word[j: n - j]
            le, ri = part + word, word + part
            if is_tandem(le):
                left.append(part)
            if is_tandem(ri):
                right.append(part)
        
        for el in left:
            for num in count[el]:
                if  i + 1 == num:
                    continue
                res.add((num, i + 1))
        for el in right:
            for num in count[el]:
                if i + 1 == num:
                    continue
                res.add((i + 1, num))
    
    return sorted(res)





def main():
    n = int(input())
    kit = [input() for _ in range(n)]
    res = calc_pairs(kit)
    
    for pair in res:
        print(*pair)


if __name__ == "__main__":
    main()