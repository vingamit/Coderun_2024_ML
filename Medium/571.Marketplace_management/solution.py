from typing import List


def calc_after_delivery(arr: List[int], curiers: int):
    m = len(arr)

    if sum(arr) <= curiers:
        return [0] * len(arr)

    while curiers > 0:
        for j in range(m):
            if arr[j] > 0:
                arr[j] -= 1
                curiers -= 1

    return arr


def main():
    m, s = map(int, input().split())
    n = int(input())

    avg = [0] * m
    res = [0] * m
    type_2 = 0

    for _ in range(n):
        mas = list(map(int, input().split()))
        arr = calc_after_delivery(mas[3:], s)
        for j in range(m):
            avg[j] += arr[j]

    q = int(input())

    for _ in range(q):
        line = list(map(int, input().split()))
        if line[0] == 1:
            arr = calc_after_delivery(line[4:], s)
            for j in range(m):
                avg[j] += arr[j]
            n += 1
        else:
            type_2 += 1
            for j in range(m):
                res[j] += avg[j] / n
    
    print(*(val / type_2 for val in res))


if __name__ == "__main__":
    main()