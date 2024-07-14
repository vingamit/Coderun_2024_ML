import sys
from math import gcd
from typing import List, Tuple


def cacl_similarity(
    n: int,
    pseq: List[int], 
    vseq: List[int]
) -> Tuple[int, int]:

    q = n * (n - 1) // 2
    p = 0

    p_dict = {i: set() for i in set(pseq)}
    v_dict = {j: set() for j in set(vseq)}

    for i, (pe, va) in enumerate(zip(pseq, vseq)):
        fi, se = p_dict[pe], v_dict[va]
        inter = len(fi & se)
        voided = i - (len(fi) + len(se) - inter)
        p += voided + inter
    
        p_dict[pe].add(i)
        v_dict[va].add(i)

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