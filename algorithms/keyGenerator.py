
import random
import utils.math as utils

def generateRsaKeys():
    """
    Passo a passo para geração de chave RSA
    1. Defina P e Q (dois números primos grandes)
    2. Calcule o valor de N = P * Q
    3. Encontre o valor Z = (P-1)*(Q-1)
    4. Defina D (Valor primo entre P e Q): inverso multiplicativo de E
        Algoritmo de euclides extendido e inverso multiplicativo
    5. Encontrar E tal que E*D mod Z = 1, sendo E e D primos

    - Chaves públicas são: N e E
    - Chaves privadas são: P, Q e ((D))

    Passo a passo para encriptar
    (C^E) MOD N para todo caractere C em texto plano
    - C: valor na tabela ASCII

    Passo a passo para decriptar
    (H^D) MOD N para todo caractere H em texto cifrado
    - H: valor na tabela ASCII
    """
    p = utils.generateLargePrime(1024)
    q = utils.generateLargePrime(1024)
    while p == q:
        q = utils.generateLargePrime(1024)
    z = (p-1)*(q-1)
    e, d = utils.findEAndD(z)
    n = p * q

    rsaKeys = {
        'public': {
            'n': n,
            'e': e
        },
        'private': {
            'd': d,
            'n': n
        }
    }

    return rsaKeys

def generateAesKey(bits):
    """Gera uma chave aleatória com a quantidade de bits no parâmetro da função."""
    key = [random.getrandbits(8) for _ in range(16)]
    return key


