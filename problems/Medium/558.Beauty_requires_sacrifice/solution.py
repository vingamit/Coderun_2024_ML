from typing import List
import numpy as np


def calc(i, k, mas: np.ndarray) -> List[int]:
    if mas[i][0] == 1 and mas[i][1] <= k:
        return [i]
    
    p = mas[:, 0]
    c = mas[:, 1]
    cord = mas[:, 2:]

    dist = np.sum((cord - mas[i, 2:]) ** 2, axis=1)
    res = []

    for j, (pi, ci, di) in enumerate(zip(p, c, dist)):
        if pi == 1 and ci <= k:
            res.append((di, j))
    
    res.sort()

    return [j for _, j in res[:5]]


def main():
    n, q = map(int, input().split())

    mas = list(list(map(int, input().split())) for _ in range(n))
    mas = np.array(mas)

    ik = list(list(map(int, input().split())) for _ in range(q))

    for i, k in ik:
        res = calc(i, k, mas)
        print(len(res), *res)



if __name__ == "__main__":
    main()