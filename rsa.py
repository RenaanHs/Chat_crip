import random
from math import gcd

def is_prime(n):
    """Teste simples de primalidade."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5)+1):
        if n % i == 0:
            return False
    return True

def generate_prime_candidate(start=100, end=300):
    """Gera um número primo aleatório."""
    while True:
        p = random.randint(start, end)
        if is_prime(p):
            return p

def egcd(a, b):
    """Algoritmo de Euclides Estendido."""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(e, phi):
    """Inverso modular de e mod phi."""
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise Exception('Inverso modular não existe')
    else:
        return x % phi

def generate_keypair():
    """Gera par de chaves RSA (pública e privada)."""
    p = generate_prime_candidate()
    q = generate_prime_candidate()
    while q == p:
        q = generate_prime_candidate()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = modinv(e, phi)
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    """Criptografa a mensagem."""
    key, n = pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    """Descriptografa a mensagem."""
    key, n = pk
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)
