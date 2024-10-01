import sys
from math import gcd
from typing import List, Tuple
from collections import defaultdict


def cacl_similarity(
    n: int,
    pseq: List[int], 
    vseq: List[int]
) -> Tuple[int, int]:

    q = n * (n - 1) // 2
    p = q

    p_count = defaultdict(int)
    v_count = defaultdict(int)
    pv_count = defaultdict(int)

    for i in range(n):
        p_class, v_class = pseq[i], vseq[i]

        p -= p_count[p_class] - pv_count[(p_class, v_class)]
        p -= v_count[v_class] - pv_count[(p_class, v_class)]

        p_count[p_class] += 1
        v_count[v_class] += 1
        pv_count[(p_class, v_class)] += 1

    common = gcd(p, q)

    return p // common, q // common




def main():
    n = int(sys.stdin.readline().rstrip())
    p_mas = list(map(int, sys.stdin.readline().rstrip().split()))
    v_mas = list(map(int, sys.stdin.readline().rstrip().split()))

    p, q = cacl_similarity(n, p_mas, v_mas)
    print(f"{p}/{q}")

if __name__ == "__main__":
    main()