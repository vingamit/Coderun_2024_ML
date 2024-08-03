import sys
from typing import List, Tuple

sys.setrecursionlimit(100000)


def calc_cats_number(
    pos: List[List[int]]
) -> Tuple[int, List[List[int]]]:
    n = len(pos)
    m = len(pos[0])
    result_graph = [[0 for _ in range(m)] for _ in range(n)]
    visited = [[False for _ in range(m)] for _ in range(n)]
    color = 2


    def dfs(i, j, color):
        if i < 0 or i >= n or j < 0 or j >= m or visited[i][j] or pos[i][j] == 0:
            return
        if pos[i][j] == 1:
            visited[i][j] = True
            result_graph[i][j] = color
        dfs(i, j + 1, color)
        dfs(i, j - 1, color)
        dfs(i + 1, j, color)
        dfs(i - 1, j, color)
    
    for i in range(n):
        for j in range(m):
            if pos[i][j] == 1 and not visited[i][j]:
                dfs(i, j, color)
                color += 1
    
    return color - 2, result_graph


def main():
    lines = sys.stdin.readlines()
    matrix = [list(map(int, line.rstrip().split())) for line in lines]
    colors, graph = calc_cats_number(matrix)
    print(colors)
    for row in graph:
        print(*row)


if __name__ == "__main__":
    main()