from math import modf, log10, floor
from numbers import Number

TEN = (2, 5)


def factorize(num: int):
    """
    Takes a positive integer and returns a
    list of its prime factorization excluding
    1 (unless the number is 1).
    """
    primes = (2, 3, 5, 7, 9, 13, 17, 19, 23, 29)
    factors = []
    if num is 1:
        return [1, ]
    for prime in primes:
        while prime <= num and num % prime is 0:
            factors.append(prime)
            num = int(round(num / prime))
    return factors


class Fraction(Number):
    numer: list = []
    denom: list = []
    neg: bool = False

    def __init__(self, numer=0, denom=1):
        """
        A numerator and denominator with a net sign.
        numer and denom are lists of prime factors.
        If numer is a float, assumes denom is 1.
        """
        # If initialized with a decimal value:
        if isinstance(numer, float):
            if numer is 0.0:
                self.numer = 0
                self.denom = 1
            else:
                if numer < 0:
                    numer = abs(numer)
                    self.neg = True
                cmp = 0
                while (10 ** cmp) & numer is not 0:
                    cmp -= 1
                numer = int(round(numer * 10 ** -cmp))
                self.denom = [2, 5] * -cmp
                self.numer = factorize(numer)

        # If initialized with a numerator and denominator:
        elif isinstance(numer, int) and isinstance(denom, int):
            self.neg = (numer < 0) ^ (denom < 0)
            numer = abs(numer)
            denom = abs(denom)
            self.numer = factorize(numer)
            self.denom = factorize(denom)
        # cleanup:
        self.simplify()

    def simplify(self):
        """Assumes that numer and denom are prime numbers."""
        self.numer.sort()
        self.denom.sort()
        for prime in set(self.numer):
            count = min(self.denom.count(prime),
                        self.numer.count(prime))
            for i in range(count):
                self.numer.remove(prime)
                self.denom.remove(prime)
