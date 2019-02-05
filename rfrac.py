from functools import reduce
from operator import mul


def __prime_factors(start=2):
    factors = [2]
    num = start
    bound = 10000
    while num < bound:
        if not any(map(lambda fac: num % fac == 0, factors)):
            factors.append(num)
        num += 1
    for i in range(0, int(bound / 10), 10):
        print(factors[i: i + 10])


class RationalFrac:
    """
    A rational-valued fraction.

    Consists of two lists of integer-valued prime factors-
    one for the numerator, and one for the denominator.
    Each operation preserves that the fraction is simplified.
    -- numer:   [int, ] = []      empty if numerator is 1.
    -- denom:   [int, ] = []      empty if denominator is 1.
    -- neg:     bool = False      True if net sign is negative.
    """

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

        if numer == 0:
            self.numer = [0, ]
            return

        # If initialized with a float:
        elif isinstance(numer, float):
            if numer < 0.0:
                self.neg = True
                numer = abs(numer)
            exp = len(str(numer).split('.')[1])
            # numer = int(str(numer).split('.')[1])

            numer = int(round(numer * 10 ** exp))
            self.numer = RationalFrac.factorize(numer)
            self.denom = [2, 5] * exp

        # If initialized with a numerator and denominator:
        elif isinstance(numer, int) and isinstance(denom, int):
            self.numer = RationalFrac.factorize(abs(numer))
            self.denom = RationalFrac.factorize(abs(denom))
            self.neg = not ((numer < 0) == (denom < 0))
            if denom == 0:
                raise ZeroDivisionError(
                    'should not initialize with a denominator of zero.')

        # If initialized with a string version of a fraction:
        elif isinstance(numer, str):
            split = numer.strip().split('/')
            self.__init__(int(split[0]), int(split[1]))

        # Unexpected argument as initialization value:
        else:
            raise TypeError(
                'could not create a rational '
                'fraction with the given parameters')

        # If successful, cleanup:
        self.simplify()

    def __copy__(self):
        """ Returns a copy of this RationalFrac object. """
        copy = RationalFrac(0, empty=True)
        copy.numer = self.numer.copy()
        copy.denom = self.denom.copy()
        copy.neg = bool(self.neg)
        return copy

    @staticmethod
    def factorize(num: int) -> [int, ]:
        """
        Takes a positive integer and returns a
        list of its prime factors excluding 1
        (unless the number is 1).
        """
        # assert isinstance(num, int)
        primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                  31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                  73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
                  127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
                  179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                  233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
                  283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
                  353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
                  419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
                  467, 479, 487, 491, 499, 503, 509, 521, 523, 541)
        factors = []
        if num == 0:
            return [0, ]

        # Generate a list of prime factors:
        for prime in primes:
            if prime > num:
                break
            while num % prime == 0:
                factors.append(prime)
                num = int(round(num / prime))
        if num != 1:
            # TODO: make it find larger primes to avoid this problem.
            raise ArithmeticError(
                f'num is {num}. did not finish prime factorization.')
        return factors

    @staticmethod
    def rf_prod(prime_factors: [int, ]):
        """
        Returns the product of a list of prime factors.
        assumes the only prime factors is one if and only
        if the list of primes is empty. Returns 0 if it
        exists in the list of primes.
        """
        return 1 if not prime_factors else reduce(mul, prime_factors, 1)

    def simplify(self):
        """
        Used to maintain that numer and
        denom have no common factors.
        Assumes that numer and denom
        are lists of prime numbers.
        """
        if 0 in self.numer:
            self.numer = [0, ]
            self.denom = []
            self.neg = False
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

    def numer_prod(self) -> int:
        return RationalFrac.rf_prod(self.numer)

    def denom_prod(self) -> int:
        return RationalFrac.rf_prod(self.denom)

    """
    Public-use, representation/observer methods:
    """
    def __float__(self) -> float:
        """Public method to get the float value of this fraction."""
        val = self.numer_prod() / self.denom_prod()
        return -val if self.neg else val

    def __int__(self) -> int:
        """Public method to get the int value of this fraction."""
        # If denominator is 1:
        if self.denom:
            return (-self.numer_prod() if self.neg
                    else self.numer_prod())
        else:
            return int(self.__float__())

    def __str__(self, fmt='') -> str:
        s = '-' if self.neg else ' ' if ' ' in fmt else ''
        if 0 in self.numer:
            s += '0'
        elif 0 in self.denom:
            s += 'undef'
        else:
            s += '%d' % self.numer_prod()
            if self.denom:
                s += '/%d' % self.denom_prod()
        return s

    def __repr__(self) -> str:
        """
        Same as __str__, but always prints
        the sign and the denominator.
        """
        s = '-' if self.neg else '+'
        if 0 in self.numer:
            s += '0'
        elif 0 in self.denom:
            s += 'undef'
        else:
            s += '%d/%d' % (self.numer_prod(),
                            self.denom_prod())
        return s

    """
    Addition and Subtraction:
    """
    def __add__(self, other):
        """Returns the sum of this fraction and other."""
        if isinstance(other, RationalFrac):
            if 0 in self.denom or 0 in other.denom:
                raise ZeroDivisionError(
                    'cannot add when either ' +
                    'operand is undefined.')

            # Get denominator factors not shared
            # for self and other respectively:
            diff_self = self.denom.copy()
            diff_other = other.denom.copy()
            for factor in self.denom:
                if factor in diff_self and factor in diff_other:
                    diff_self.remove(factor)
                    diff_other.remove(factor)

            # Calculate the new numerator:
            numer_self = RationalFrac.rf_prod(self.numer + diff_other)
            numer_other = RationalFrac.rf_prod(other.numer + diff_self)
            if self.neg:
                numer_self *= -1
            if other.neg:
                numer_other *= -1
            numer = numer_self + numer_other

            # Create the new fraction:
            fsum = RationalFrac(0, empty=True)
            fsum.numer = RationalFrac.factorize(abs(numer))
            fsum.denom = self.denom + diff_other
            fsum.neg = numer < 0
            fsum.simplify()
            return fsum

        elif isinstance(other, (int, float)):
            return self.__add__(RationalFrac(other))
        else:
            return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (int, float)):
            return self.__add__(RationalFrac(other))
        else:
            return NotImplemented

    def __sub__(self, other):
        """Returns the difference between this fraction and other."""
        return self.__add__(other.__neg__())

    """
    Multiplication, Division:
    """
    def reciprocal(self):
        """
        Returns a reciprocal view of this fraction.
        This is an important function, as it enforces
        the representation of an integer-valued RationalFrac
        as having an empty list as its denom field.
        """
        recip = RationalFrac(0, empty=True)
        if 0 in self.numer:
            raise ZeroDivisionError('the reciprocal of zero is undefined.')
        recip.numer = self.denom.copy()
        recip.denom = self.numer.copy()
        recip.neg = bool(self.neg)
        return recip

    def __neg__(self):
        negated = self.__copy__()
        negated.neg = not self.neg if (0 in self.numer) else False
        return negated

    def __mul__(self, other):
        """ Returns the product of this and another fraction. """
        if isinstance(other, (int, float, str)):
            other = RationalFrac(other)
        if isinstance(other, RationalFrac):
            prod = RationalFrac(0, empty=True)
            prod.numer = self.numer + other.numer
            prod.denom = self.denom + other.denom
            prod.neg = not (self.neg == other.neg)
            prod.simplify()
            return prod
        else:
            return NotImplemented

    def __imul__(self, other):
        """ Multiplies self by other(a constant) in-place. """
        if isinstance(other, (int, float, str)):
            other = RationalFrac(other)
        if isinstance(other, RationalFrac):
            self.numer.extend(other.numer)
            self.denom.extend(other.denom)
            self.neg = not(self.neg == other.neg)
            self.simplify()
            return self
        else:
            return NotImplemented

    def __rmul__(self, other):
        """ Returns the product of this and a constant. """
        if isinstance(other, (int, float, str)):
            return self.__mul__(RationalFrac(other))
        else:
            return NotImplemented

    def __truediv__(self, other):
        """ Returns the quotient of this and another fraction. """
        if isinstance(other, (int, float, str)):
            other = RationalFrac(other)
        if isinstance(other, RationalFrac):
            quot = RationalFrac(0, empty=True)
            quot.numer = self.numer + other.denom
            quot.denom = self.denom + other.numer
            quot.neg = not (self.neg == other.neg)
            quot.simplify()
            return quot
        else:
            return NotImplemented

    def __itruediv__(self, other):
        """ Divides self by other in place. """
        if isinstance(other, (int, float, str)):
            other = RationalFrac(other)
        if isinstance(other, RationalFrac):
            self.numer.extend(other.denom)
            self.denom.extend(other.numer)
            self.neg = not(self.neg == other.neg)
            self.simplify()
            return self
        else:
            return NotImplemented

    """
    Modulus and powers:
    """
    def mixed(self):
        """
        Removes the whole-number part of
        this fraction and returns it.
        """
        numer = self.numer_prod()
        denom = self.denom_prod()
        self.numer = RationalFrac.factorize(numer % denom)
        return numer // denom

    def __pow__(self, power, modulo=None):
        """
        Returns this fraction to the specified power.
        Requires that power has an equivalent integer value.
        """
        if isinstance(power, int):
            if power == 0:
                return RationalFrac(1)
            elif power < 0:
                fexp = self.reciprocal()
                power = abs(power)
            else:
                fexp = self.__copy__()

            fexp.numer *= power
            fexp.denom *= power
            fexp.neg = (power % 2 == 1) if self.neg else False
            return fexp

        elif isinstance(power, RationalFrac):
            assert not power.denom, 'expected integer-valued power'
            return self.__pow__(int(power))
        else:
            return NotImplemented

    def __rpow__(self, other):
        """
        Returns other ** self.
        The return type is MonoFrac.
        """
        pass  # TODO: implement this.

    """
    Rich comparison methods:
    """
    def __eq__(self, other):
        """
        Returns True if the fractions are equal in value.
        Assumes the rep invariant that both are fully simplified.
        """
        if isinstance(other, RationalFrac):
            return (self.numer == other.numer and
                    self.denom == other.denom and
                    self.neg == other.neg)
        elif isinstance(other, (int, float, str)):
            return self.__eq__(RationalFrac(other))
        else:
            return NotImplemented

    def __lt__(self, other):
        """ Returns True if the fractions are equal in value. """
        if isinstance(other, RationalFrac):
            # NOTE: neg is False when 0 in numer.
            return (self - other).neg
        elif isinstance(other, (int, float, str)):
            return (self - (RationalFrac(other))).neg
        else:
            return NotImplemented


def rational_frac_tests():
    """ Some small test cases for the RationalFrac class. """
    print('\n==========================================')
    print('rfrac.py @ rational_frac_tests: //////////\n')
    print(RationalFrac(-1), RationalFrac(0))
    # __prime_factors()
    frac0 = RationalFrac(4.5)
    frac1 = RationalFrac(-0.125)
    frac2 = RationalFrac(0.99999)
    f = [frac0, frac1, frac2]
    print('float(-0.125) =', float(f[1]))
    print('float(0.99999) =', float(f[2]))
    print('9/2 + -1/8 =', f[0] + f[1])
    print('9/2 * -1/8 =', f[0] * f[1])
    print('-1/8 * 9/2 =', f[1] * f[0])
    print(f)
    print('frac(-0/1) + frac(-0/1) =',
          RationalFrac(-0) + RationalFrac(-0))
    f3 = RationalFrac('-7/29')
    print(f3)
    print('\nrfrac.py @ end of rational_frac_tests ////')
    print('==========================================\n')


if __name__ == '__main__':
    rational_frac_tests()
