from math import sqrt, gcd


def isqrt(n):
    return int(sqrt(n))


def factorize(n):
    if n == 1:
        return tuple()
    factors = []
    for i in range(2, isqrt(n) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    return tuple(factors)


def count_square_tuples(k, m):
    numbers = [factorize(i) for i in range(1, k + 1)]
    
    all_primes = sorted(set(factor for num in numbers for factor in num))
    prime_to_index = {p: i for i, p in enumerate(all_primes)}
    
    dp = [[0] * (1 << len(all_primes)) for _ in range(m + 1)]
    dp[0][0] = 1
    
    for i in range(1, m + 1):
        for num in numbers:
            for mask in range(1 << len(all_primes)):
                new_mask = mask
                for p in num:
                    new_mask ^= 1 << prime_to_index[p]
                dp[i][new_mask] += dp[i-1][mask]
    
    return dp[m][0]


def mod_inverse(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m


def main():
    MOD = 1000000007
    m, k = map(int, input().split())
    num = count_square_tuples(k, m)
    deno = k ** m
    GCD = gcd(num, deno)
    p, q = num // GCD, deno // GCD
    q_inv = mod_inverse(q, MOD)
    result = (p * q_inv) % MOD
    print(result)


if __name__ == "__main__":
    main()