from typing import Iterable, List
from functools import reduce
from operator import mul
from local.ec.core import MAX_COORDINATE, NUMBER_POINTS
import random
import math
import unittest


def miller_rabin(n: int, k: int) -> bool:
    """
    Return whether n is probably prime after k rounds.

    Uses the Miller-Rabin primality test.
    https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test

    Probability that composite number is declared prime after k rounds:
    Pr(MR_k | ¬P) <= 4 ** (-k)

    Probability that uniform random number between 0 and n is prime:
    Pr(P_n) = log(n) / n
    https://en.wikipedia.org/wiki/Prime_number_theorem

    Probability that declared prime (<= n) is in fact composite after k rounds:
    Pr(¬P | MR_k) < Pr(MR_k | ¬P) * (1 / Pr(P_n) - 1)

    For n <= 1000:
    Pr(¬P | MR_1)  < 0.002
    Pr(¬P | MR_2)  < 0.0004
    Pr(¬P | MR_5)  < 6.74 * 10**(-6)
    Pr(¬P | MR_10) < 6.58 * 10**(-9)
    """
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    # Factor out powers of 2 to find s > 0 and d > 0
    # such that n - 1 = d * 2^s with d odd
    d, s = n - 1, 0
    while d % 2 == 0:
        s += 1
        d //= 2
    assert n - 1 == d * 2 ** s

    for _ in range(0, k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        y = 0

        for _ in range(0, s):
            y = pow(x, 2, n)
            if y == 1 and x != 1 and x != n - 1:
                return False
            x = y

        if y != 1:
            return False

    return True


def trial_division(n: int) -> bool:
    """
    Return whether n is provably prime.

    Uses a simple optimized trial division method.
    https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    limit = math.isqrt(n)
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def is_prime(n: int) -> bool:
    """
    Return whether n is prime.
    """
    return miller_rabin(n, 5)


def euler_totient(factors: Iterable[int]) -> int:
    """
    Compute Euler's totient function of integer n whose prime factorization is given.

    **The method assumes that the given factors are prime numbers!**
    """
    n = reduce(mul, factors, 1)
    return int(n * reduce(mul, [1 - 1 / p for p in set(factors)], 1))


def is_coprime(a: int, factors: Iterable[int]) -> bool:
    """
    Check if integer a is a coprime of integer n whose prime factorization is given.

    **The method assumes that the given factors are prime numbers!**
    """
    return all(a % p != 0 for p in factors)


def get_coprimes(factors: Iterable[int]) -> List[int]:
    """
    Return the list of coprimes of integer n whose prime factorization is given.

    This is equivalent to the elements of the multiplicative group of integers modulo n.

    **The method assumes that the given factors are prime numbers!**
    """
    n = reduce(mul, factors, 1)
    return [a for a in range(1, n) if is_coprime(a, factors)]


def get_coprime(factors: Iterable[int]) -> int:
    """
    Return a random coprime of integer n whose prime factorization is given.

    **The method assumes that the given factors are prime numbers!**
    """
    n = reduce(mul, factors, 1)
    while True:
        a = random.randrange(1, n)
        if is_coprime(a, factors):
            return a


class TestPrimes(unittest.TestCase):
    primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
        101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
        199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
        317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
        443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571,
        577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
        701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829,
        839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977,
        983, 991, 997
    ]
    euler_totients = [
        1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4, 12, 6, 8, 8, 16, 6, 18, 8, 12, 10, 22, 8, 20, 12, 18, 12, 28, 8, 30, 16,
        20, 16, 24, 12, 36, 18, 24, 16, 40, 12, 42, 20, 24, 22, 46, 16, 42, 20, 32, 24, 52, 18, 40, 24, 36, 28, 58, 16,
        60, 30, 36, 32, 48, 20, 66, 32, 44, 24, 70, 24, 72, 36, 40, 36, 60, 24, 78, 32, 54, 40, 82, 24, 64, 42, 56, 40,
        88, 24, 72, 44, 60, 46, 72, 32, 96, 42, 60, 40
    ]

    def test_trial_division(self):
        for n in range(0, 1000):
            self.assertEqual(n in self.primes, trial_division(n))

    def test_miller_rabin(self):
        for n in range(0, 1000):
            provably_prime = n in self.primes
            probably_prime = miller_rabin(n, 2)

            if provably_prime:
                self.assertTrue(probably_prime)
            if not probably_prime:
                self.assertFalse(provably_prime)

            if provably_prime and (not probably_prime):
                print("false negative: {}".format(n))
            if probably_prime and (not provably_prime):
                print("false positive: {}".format(n))

    def test_max_coordinate_is_prime(self):
        self.assertTrue(is_prime(MAX_COORDINATE))

    def test_number_points_is_prime(self):
        self.assertTrue(is_prime(NUMBER_POINTS))

    def test_euler_totient(self):
        primes = [p for p in self.primes if p < 100]

        for a in primes:
            self.assertEqual(self.euler_totients[a - 1], euler_totient([a]))
            for b in primes:
                if a * b > 100:
                    break
                self.assertEqual(self.euler_totients[a * b - 1], euler_totient([a, b]))
                for c in primes:
                    if a * b * c > 100:
                        break
                    self.assertEqual(self.euler_totients[a * b * c - 1], euler_totient([a, b, c]))

    def test_get_coprimes(self):
        primes = [p for p in self.primes if p < 100]

        for a in primes:
            for b in primes:
                n = a * b
                z_n_star = [i for i in range(n) if math.gcd(i, n) == 1]
                self.assertEqual(z_n_star, get_coprimes([a, b]))
