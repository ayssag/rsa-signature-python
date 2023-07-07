from math import gcd
import random

def extendedGcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extendedGcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modularInverse(a, m):
    g, x, y = extendedGcd(a, m)
    return x % m

def findEAndD(z):
    for e in range(2, z):
        if gcd(e, z) == 1:
            d = modularInverse(e, z)
            return e, d
    return None, None

def isPrime(n, k=5):
    """Teste de primalidade de Miller-Rabin"""
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # Representar n - 1 como 2^r * d, onde d é ímpar
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Executar k iterações do teste
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def generateLargePrime(bits):
    while True:
        num = random.getrandbits(bits)
        if num % 2 == 0:
            num += 1  # Garantir que o número gerado seja ímpar

        if isPrime(num):
            return num

