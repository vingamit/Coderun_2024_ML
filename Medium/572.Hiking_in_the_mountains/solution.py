from typing import List


def calc_max_pos_time(n: int, s: int, seq: List[int]) -> str:
    if len(seq) <= s:
        return 'INF'
    tsor = sorted(seq)
    ans = float('inf')
    for i in range(n - s):
        diff = tsor[s + i] - tsor[i]
        if diff < ans:
            ans = diff
    if ans == 0:
        return "Impossible"
    return str(ans)


def main():
    n, s = map(int, input().split())
    mas_t = [int(input()) for _ in range(n)]
    print(calc_max_pos_time(n, s, mas_t))


if __name__ == "__main__":
    main()