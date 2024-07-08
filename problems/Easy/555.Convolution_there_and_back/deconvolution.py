import numpy as np
from scipy import linalg


def calc_B(A: np.ndarray, C: np.ndarray) -> np.ndarray:
    n, m = A.shape
    p, q = C.shape
    k = n - p + 1

    equations = []
    b_values = []

    for i in range(p):
        for j in range(q):
            eq = np.zeros((k, k))
            for x in range(k):
                for y in range(k):
                    eq[x, y] = A[i+x, j+y]
            equations.append(eq.flatten())
            b_values.append(C[i, j])

    equations = np.array(equations)
    b_values = np.array(b_values)

    B_flat = linalg.lstsq(equations, b_values)[0]
    B = np.round(B_flat.reshape((k, k))).astype(int)

    return B


def main():
    n, m, k = map(int, input().split())
    A = np.array([list(map(int, input().split())) for _ in range(n)])
    C = np.array([list(map(int, input().split())) for _ in range(n - k + 1)])

    B = calc_B(A, C)

    for row in B:
        print(*row.tolist())

if __name__ == "__main__":
    main()