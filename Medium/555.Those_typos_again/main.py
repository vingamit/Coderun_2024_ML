def LevDistBounded(a, b, k):
    n = len(a)
    m = len(b)

    if abs(m - n) > k:
        return k + 1
    
    fill_bound = min(m, k)
    previous = list(range(fill_bound + 1)) + [float('inf')] * (m - fill_bound)
    current = [float('inf')] * (m + 1)

    for i in range(n):
        current[0] = i + 1

        # compute stripe indices
        stripe_start = max(0, i - k)
        stripe_end = min(m, i + k + 1)

        # ignore entry left of leftmost
        if stripe_start > 0:
            current[stripe_start] = float('inf')

        # loop through stripe
        for j in range(stripe_start, stripe_end):
            indicator = 1 if a[i] != b[j] else 0

            current[j + 1] = min(
                previous[j + 1] + 1,  # deletion
                current[j] + 1,       # insertion
                previous[j] + indicator  # substitution
            )

        previous, current = current, previous

    return previous[m]

def optim(a, b, k):
    i = 0
    n = min(len(a), len(b))
    while i < n and a[i] == b[i]:
        i += 1
    a, b = a[i:], b[i:]

    n = min(len(a), len(b))
    j = 0
    while j < n and a[-(j + 1)] == b[-(j + 1)]:
        j += 1

    a, b = a[:len(a) - j], b[:len(b) - j]
    
    if len(a) == 0:
        return len(b)
    
    if len(b) == 0:
        return len(a)
    
    return LevDistBounded(a, b, k)
    

def main():
    t = int(input())
    
    res = []
    for _ in range(t):
        k = int(input())
        s, t = input(), input()
        distance = LevDistBounded(s, t, k)
        if distance <= k:
            res.append("Yes")
        else:
            res.append("No")
    
    print('\n'.join(res))


if __name__ == "__main__":
    main()