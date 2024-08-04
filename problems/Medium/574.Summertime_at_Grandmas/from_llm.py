from itertools import product
from math import gcd

MOD = 1000000007

def is_perfect_square(n):
    return int(n ** 0.5) ** 2 == n

def count_favorable_outcomes(m, k):
    favorable = 0
    for outcome in product(range(1, k + 1), repeat=m):
        if is_perfect_square(prod(outcome)):
            favorable += 1
    return favorable

def prod(iterable):
    result = 1
    for i in iterable:
        result *= i
    return result

def solve(m, k):
    favorable = count_favorable_outcomes(m, k)
    total = k ** m
    return favorable
    print(favorable, total)
    
    # Сокращаем дробь
    g = gcd(favorable, total)
    p, q = favorable // g, total // g
    
    # Находим модульное обратное для q
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
    q_inv = mod_inverse(q, MOD)
    result = (p * q_inv) % MOD
    
    return result

# Чтение входных данных
val = 'm/k'
print(f'{val:-^7}',*(f'{val:-^7}' for val in range(3, 21)))
for m in range(1, 21):
    print(f"{m:-^7}", *(f'{solve(m, k):-<7}' for k in range(3, 21)))
# Вывод результата
# for m in range(1, 10):
#     solve(m, k)
