from typing import List


def conv_slow(
    A: List[List[int]],
    B: List[List[int]]
) -> List[List[int]]:
    n, m = len(A), len(A[0])
    k = len(B)

    res = []
    for i in range(n - k + 1):
        res.append([])
        row: List[int] = res[-1]
        for j in range(m - k + 1):
            sum = 0
            for t in range(k):
                for l in range(k):
                    sum += A[i+t][j+l] * B[t][l]
            row.append(sum)

    
    return res


def main():
    n, m = map(int, input().split())
    mas_a = [list(map(int, input().split())) for _ in range(n)]
    k = int(input())
    kernel = [list(map(int, input().split())) for _ in range(k)]
    
    res = conv_slow(mas_a, kernel)

    for row in res:
        print(' '.join(str(numbers) for numbers in row))


if __name__ == "__main__":
    main()