from typing import List


def tape_issuing(
    n: int, 
    k: int, 
    themes: List[str], 
    themes_id: List[int]
) -> List[str]:
    
    tape = []

    taken = {}

    for theme, theme_id in zip(themes, themes_id):
        taken[theme] = taken.get(theme, 0) + 1
        if taken[theme]> k:
            continue
        if len(tape) == n:
            break
        recomendation = f"{theme} #{theme_id}"
        tape.append(recomendation)
    
    return tape


def main():
    p, n, k = map(int, input().split())
    themes = [input() for _ in range(p)]
    themes_id = list(map(int, input().split()))

    tape = tape_issuing(n, k, themes, themes_id)

    print(*tape, sep='\n')


if __name__ == "__main__":
    main()