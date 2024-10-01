import sys
from typing import List


def check_in(stop_words: List[str], message) -> str:
    for word in stop_words:
        if word in message:
            return "DELETE"
    return "KEEP"


def main():
    n, m = map(int, sys.stdin.readline().rstrip().split())

    stop = [sys.stdin.readline().rstrip() for _ in range(n)]
    messages = [sys.stdin.readline().rstrip() for _ in range(m)]

    results = []
    for message in messages:
        result = check_in(stop, message)
        results.append(result)
    
    print("\n".join(results))
        

if __name__ == "__main__":
    main()