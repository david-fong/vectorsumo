from functools import reduce
from math import floor
from numbers import Number
from operator import mul


def factorize(num: int) -> [int, ]:
    """
    Takes a positive integer and returns a
    list of its prime factors excluding 1
    (unless the number is 1).
    """
    primes = (2, 3, 5, 7, 9, 11, 13, 17, 19, 23, 29,
              31, 37, 41, 43, 47, 53, 59, 61, 71,
              79, 83, 89, 97, 101, 103, 107, 109,
              113, 127, 131, 137, 139, 149, 151,
              157, 163, 167, 173, 179, 181, 191,
              193, 197, 199, 211, 223, 227, 229)
    factors = []
    if num is 1:
        return [1, ]
    for prime in primes:
        if prime > num:
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


class Fraction(dict):
    """
    A real-valued fraction.
    Consists of a single dict from prime factors,
        to their powers, which are rational fractions.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RationalFrac:
    """
    A rational-valued fraction.
    Consists of two lists of integer-valued prime factors-
        one for the numerator, and one for the denominator.
    Each operation preserves that the fraction is simplified.
    """
    numer: [int, ] = []
    denom: [int, ] = []
    neg: bool = False

    def __init__(self, numer, denom=1, empty=False):
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

        # If copy constructing another Fraction:
        if isinstance(numer, RationalFrac):
            self.numer = numer.numer
            self.denom = numer.denom
            self.neg = numer.neg
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
                while (10 ** cmp) < (1 / (numer - int(floor(numer)))):
                    cmp += 1
                numer = int(round(numer * (10 ** cmp)))
                self.numer = factorize(numer)
                self.denom = [2, 5] * cmp

        # If initialized with a numerator and denominator:
        elif isinstance(numer, int) and isinstance(denom, int):
            self.neg = not ((numer < 0) is (denom < 0))
            self.numer = factorize(abs(numer)) \
                if numer is not 0 else [0, ]
            self.denom = factorize(abs(denom))

        else:
            raise TypeError(
                'could not create a rational ' +
                'fraction with given parameters')
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
            self.denom = [1, ]
            return
        elif 0 in self.denom:
            self.denom = [0, ]
            return

        # Eliminate common factors:
        for factor in set(self.numer):
            # number of shared occurrences:
            count = min(self.denom.count(factor),
                        self.numer.count(factor))
            # Remove each shared occurrence:
            for i in range(count):
                self.numer.remove(factor)
                self.denom.remove(factor)

        if len(self.numer) == 0:
            self.numer = [1, ]
        if len(self.denom) == 0:
            self.denom = [1, ]

    """
    Public-use, representation/observer methods:
    """
    def __float__(self) -> float:
        """Public method to get the float value of this fraction."""
        val = self.numer_prod() / self.denom_prod()
        return -val if self.neg else val

    def __int__(self) -> int:
        """Public method to get the int value of this fraction."""
        return int(float(self))

    def __repr__(self) -> str:
        s = '-' if self.neg else ''
        if 0 in self.numer:
            s += '0'
        elif 0 in self.denom:
            s += 'undef'
        else:
            s += '%d' % self.numer_prod()
            if 1 not in self.denom:
                s += '/%d' % self.denom_prod()
        return s

    def numer_prod(self) -> int:
        return reduce(mul, self.numer, 1)

    def denom_prod(self) -> int:
        return reduce(mul, self.denom, 1)

    """
    Negation, Addition, and Subtraction:
    """
    def __neg__(self):
        neg = RationalFrac(0, empty=True)
        neg.numer = self.numer.copy()
        neg.denom = self.denom.copy()
        neg.neg = not self.neg
        return neg

    def __add__(self, other):
        """Returns the sum of this fraction and other."""
        if isinstance(other, RationalFrac):
            if (self.denom is [0, ] or
                    other.denom is [0, ]):
                raise ZeroDivisionError
            fsum = RationalFrac(0, empty=True)

            # Get denominator factors not
            # shared for self and other:
            ds = self.denom.copy()
            do = other.denom.copy()
            for factor in self.denom:
                if factor in ds and factor in do:
                    ds.remove(factor)
                    do.remove(factor)

            numer = \
                reduce(mul, self.numer + ds, 1) + \
                reduce(mul, other.numer + do, 1)
            fsum.numer = factorize(numer)
            fsum.denom = self.denom + do
            fsum.neg = numer < 0
            fsum.simplify()
            return fsum

        elif isinstance(other, (int, float)):
            return self.__add__(RationalFrac(other))
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, (int, float)):
            return self.__add__(RationalFrac(other))
        else:
            return NotImplemented

    def __sub__(self, other):
        """Returns the difference between this fraction and other."""
        return self + -other

    """
    Multiplication, Division, and Exponents:
    """
    def reciprocal(self):
        """ Returns a reciprocal view of this fraction. """
        recip = RationalFrac(0, empty=True)
        recip.numer = self.denom.copy()
        recip.denom = self.numer.copy()
        return recip

    def __mul__(self, other):
        """ Returns the product of this and another fraction. """
        if isinstance(other, RationalFrac):
            prod = RationalFrac(0, empty=True)
            prod.numer = self.numer + other.numer
            prod.denom = self.denom + other.denom
            prod.neg = not (self.neg is other.neg)
            prod.simplify()
            return prod
        else:
            return NotImplemented

    def __imul__(self, other):
        """ Multiplies self by other(a constant) in-place. """
        if isinstance(other, (RationalFrac, float, int)):
            f_other = RationalFrac(other) if isinstance(other, RationalFrac) else other
            self.numer.extend(f_other.numer)
            self.denom.extend(f_other.denom)
            self.neg = not (self.neg is other < 1)
            self.simplify()
        else:
            return NotImplemented

    def __rmul__(self, other):
        """ Returns the product of this and a constant. """
        if isinstance(other, (int, float)):
            return RationalFrac(other) * self
        else:
            return NotImplemented

    def __truediv__(self, other):
        """ Returns the quotient of this and another fraction. """
        if isinstance(other, RationalFrac):
            return other.reciprocal() * self
        elif isinstance(other, (int, float)):
            f_other = RationalFrac(other)
            return f_other.reciprocal() * self
        else:
            return NotImplemented

    def __itruediv__(self, other):
        """ Divides self by other(a constant) in-place. """
        if isinstance(other, (RationalFrac, float, int)):
            f_other = RationalFrac(other) if isinstance(other, RationalFrac) else other
            f_other = f_other.reciprocal()

            # Same as __mul__():
            self.numer.extend(f_other.numer)
            self.denom.extend(f_other.denom)
            self.neg = not (self.neg is other < 1)
            self.simplify()
        else:
            return NotImplemented

    def __pow__(self, power, modulo=None):
        """ Returns this fraction to the specified power. """
        if power is 0:
            return RationalFrac(1)
        elif power < 0:
            fexp = self.reciprocal()
            power = abs(power)
        else:
            fexp = RationalFrac(self)

        fexp.numer *= power
        fexp.denom *= power
        fexp.neg = (power % 2 == 1) if self.neg else False
        return fexp

    """
    Rich comparison methods:
    """
    def __eq__(self, other):
        """
        Returns True if the fractions are equal in value.
        Assumes the rep invariant that both are fully simplified.
        """
        if isinstance(other, (RationalFrac, int, float)):
            f_other = RationalFrac(other) if \
                isinstance(other, (int, float)) else other

            return (self.numer == f_other.numer and
                    self.denom == f_other.denom and
                    self.neg is f_other.neg)
        else:
            return NotImplemented

    def __lt__(self, other):
        """ Returns True if the fractions are equal in value. """
        if isinstance(other, (RationalFrac, Number)):
            f_other = RationalFrac(other) if isinstance(other, Number) else other
            return (self - f_other).neg
        else:
            return NotImplemented


# test = Fraction(4.5)
# print(test)
# __prime_factors()
