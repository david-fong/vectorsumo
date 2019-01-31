from functools import reduce
from math import modf
from numbers import Number
from operator import mul

TEN = (2, 5)


def factorize(num: int):
    """
    Takes a positive integer and returns a
    list of its prime factors excluding 1
    (unless the number is 1).
    """
    primes = (2, 3, 5, 7, 9, 13, 17, 19, 23, 29,
              31, 37, 41, 43, 47, 53, 59, 61, 71,
              79, 83, 89, 97, 101, 103, 107, 109,
              113, 127, 131, 137, 139, 149, 151,
              157, 163, 167, 173, 179, 181, 191,
              193, 197, 199, 211, 223, 227, 229)
    factors = []
    if num is 1:
        return [1, ]
    for prime in primes:
        if prime >= num:
            break
        while num % prime is 0:
            factors.append(prime)
            num = int(round(num / prime))
    return factors


def __prime_factors(start=2):
    factors = [2]
    num = start
    bound = 1000
    while num < bound:
        if not any(map(lambda f: num % f is 0, factors)):
            factors.append(num)
        num += 1
    print(factors)


class Fraction:
    numer: [int, ] = []
    denom: [int, ] = []
    neg: bool = False

    def __init__(self, numer: Number, denom=1, empty=False):
        """
        A numerator and denominator with a net sign.
        numer and denom are lists of prime factors.
        If numer is a float, assumes denom is 1.

        The empty parameter should only be used privately.
        """
        # Initialize with no contents:
        # For private use only.
        if empty:
            return

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
                while (10 ** cmp) < (1 / modf(numer)[0]):
                    cmp += 1
                numer = int(round(numer * (10 ** cmp), 0))
                self.denom = ([2, ] * cmp) + ([5, ] * cmp)
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
        """
        Assumes that numer and denom
        are lists of prime numbers.
        """
        # self.numer.sort()
        # self.denom.sort()
        if 0 in self.numer:
            self.numer = [0, ]
        elif 0 in self.denom:
            self.denom = [0, ]

        # Eliminate common factors:
        for prime in set(self.numer):
            # number of shared occurrences:
            count = min(self.denom.count(prime),
                        self.numer.count(prime))
            # Remove each shared occurrence:
            for i in range(count):
                self.numer.remove(prime)
                self.denom.remove(prime)

    def val(self):
        """Public method to get the float value of this fraction."""
        return self.__numer_val() / self.__denom_val()

    def __numer_val(self):
        return reduce(mul, self.numer, 1)

    def __denom_val(self):
        return reduce(mul, self.denom, 1)

    def __repr__(self):
        s = '-' if self.neg else ' '
        if 0 in self.numer:
            s += '0'
        elif 0 in self.denom:
            s += 'inf'
        else:
            s += '%d/%d' % (self.__numer_val(),
                            self.__denom_val())
        return s

    def __add__(self, other):
        if (isinstance(other, Fraction) and
                self.denom is not [0, ] and
                other.denom is not [0, ]):
            fsum = Fraction(0)

            # Get denominator factors not
            # shared for self and other:
            ds = self.denom.copy()
            do = other.denom.copy()
            for factor in self.denom:
                if factor in ds and factor in do:
                    ds.remove(factor)
                    do.remove(factor)
            return fsum
        else:
            return NotImplemented

    def reciprocal(self):
        """Returns a reciprocal view of this fraction."""
        recip = Fraction(0, empty=True)
        recip.numer.extend(self.denom)
        recip.denom.extend(self.numer)
        return recip

    def __mul__(self, other):
        """Returns the product of this and another fraction."""
        if isinstance(other, Fraction):
            prod = Fraction(0, empty=True)
            prod.numer.extend(self.numer + other.numer)
            prod.denom.extend(self.denom + other.denom)
            prod.neg = self.neg ^ other.neg
            prod.simplify()
            return prod
        else:
            return NotImplemented

    def __rmul__(self, other):
        """Returns the product of this and a constant."""
        prod = Fraction(0, empty=True)

    def __pow__(self, power, modulo=None):
        fexp = Fraction(0, empty=True)
        pass  # TODO


# test = Fraction(4.5)
# print(test)
# __prime_factors()
