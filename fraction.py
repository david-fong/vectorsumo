from functools import reduce
from numbers import Number
from operator import mul

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

    def __init__(self, numer: Number, denom=1):
        """
        A numerator and denominator with a net sign.
        numer and denom are lists of prime factors.
        If numer is a float, assumes denom is 1.
        """
        # Copy constructor of another Fraction:
        if isinstance(numer, Fraction):
            self.numer = numer.numer
            self.denom = numer.denom

        # If initialized with a decimal value:
        elif isinstance(numer, float):
            if numer is 0.0:
                self.numer = 0
                self.denom = 1
            else:
                if numer < 0:
                    numer = abs(numer)
                    self.neg = True
                cmp = 0
                # TODO: Fix this: while 10 ** cmp < (numer)^{-1}?
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
            self.numer = factorize(numer) if numer is not 0 else [0, ]
            self.denom = factorize(denom)

        else:
            return
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

    def __repr__(self):
        s = '-' if self.neg else ' '
        s += '%d/%d' % (reduce(mul, self.numer, 1),
                        reduce(mul, self.denom, 1))
        return s

    def __add__(self, other):
        pass  # TODO:

    def inverse(self):
        temp = self.numer
        self.numer = self.denom
        self.denom = temp

    def __mul__(self, other):
        if isinstance(other, Number):
            other_f = Fraction(other)
            prod = Fraction(0)
            prod.numer.extend(self.numer + other_f.numer)
            prod.denom.extend(self.denom + other_f.denom)
            prod.simplify()
            return prod
        else:
            return NotImplemented

    def __pow__(self, power, modulo=None):
        pass  # TODO


test = Fraction(0.5)
print(test)
