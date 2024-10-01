import math

def isqrt(n):
    return int(math.sqrt(n))

def factorize(n):
    if n == 1:
        return tuple()  # 1 не имеет простых множителей
    factors = []
    for i in range(2, isqrt(n) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    return tuple(factors)

def count_square_tuples(k, m):
    # Представляем каждое число как набор его простых множителей
    numbers = [factorize(i) for i in range(1, k + 1)]
    
    # Находим все уникальные простые множители
    all_primes = sorted(set(factor for num in numbers for factor in num))
    prime_to_index = {p: i for i, p in enumerate(all_primes)}
    
    # Инициализируем динамический массив
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

val = 'm/k'
print(f'{val:-^7}',*(f'{val:-^7}' for val in range(3, 21)))
for m in range(1, 6):
    print(f"{m:-^7}", *(f'{count_square_tuples(k, m):-<7}' for k in range(3, 21)))

