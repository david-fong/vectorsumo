from functools import reduce
from operator import mul

import rfrac


RF = rfrac.RationalFrac


def irr_prod(irr):
    irr_factors = map(
        lambda base, ex: base ** float(ex), irr)
    return reduce(mul, irr_factors)


class MonoFrac:
    """
    A fraction permitting factors to RationalFrac
    valued powers, but with the unchecked constraint
    on addition and subtraction that the irrational
    parts of each operand must be the same. Designed
    for use in the Fraction class.

    Represented as a RationalFrac and a dict from
    prime factors to their powers, which are also
    RationalFrac objects. This dict represents the
    irrational part of the fraction. its value is
    maintained by a simplification operation such
    that it is in the range (-1, 1), and none of
    its factors' exponents are integer values.
    """
    rational: rfrac.RationalFrac
    irr: dict = {}

    def __init__(self, number):
        """
        Must be initialized with a rational valued
        fraction or another MonoFrac object.
        """
        # Copy construction:
        if isinstance(number, MonoFrac):
            self.rational = RF(number.rational)
            self.irr = number.irr.copy()

        # Construct with rational fraction or number:
        elif isinstance(number, (RF, int, float)):
            self.rational = RF(number)

        # Unexpected arguments:
        else:
            raise TypeError(
                str(number) +
                ' invalid. must initialize with one of:\n'
                'Fraction, RationalFrac, int, float.')

    def simplify(self):
        # Factor out any rational parts of self.irr to self.rational:
        for fac, exp in self.irr.items():
            if len(exp.denom) is 0:
                rational = [fac, ] * exp.numer_prod()
                if exp.neg:
                    self.rational.denom.extend(rational)
                else:
                    self.rational.numer.extend(rational)

    def irr_numer(self):
        """
        Return a list of positive-
        exponent irrational factors.
        """
        return list(filter(
            lambda fac, exp: not exp.neg,
            self.irr
        ))

    def irr_denom(self):
        """
        Return a list of negative-
        exponent irrational factors.
        """
        return list(filter(
            lambda fac, exp: exp.neg,
            self.irr
        ))

    def cmp_degree(self, other):
        """
        Must be used externally to check if this
        MonoFrac object can be added with other.
        """
        if isinstance(other, MonoFrac):
            return self.irr == other.irr
        elif isinstance(other, (RF, int, float)):
            return len(self.irr) == 0
        else:
            raise TypeError(
                'can only compare degrees with '
                'another MonoFrac object.')

    def __add__(self, other):
        """
        Returns the sum of this MonoFrac to other
        as a MonoFrac. If other is also a MonoFrac,
        assumes that self.cmp_degree(other) is True.
        """
        if isinstance(other, MonoFrac):
            fsum = MonoFrac(0)
            fsum.rational = self.rational + other.rational
            fsum.irr = self.irr.copy()
            return fsum
        elif isinstance(other, (RF, int, float)):
            return self.__add__(MonoFrac(other))
        else:
            return NotImplemented

    def __iadd__(self, other):
        """
        Adds other to self in place. If other is also
        a MonoFrac, assumes that self.cmp_degree(other)
        is True.
        """
        if isinstance(other, MonoFrac):
            self.rational += other.rational
            return self
        elif isinstance(other, (RF, int, float)):
            return self.__add__(MonoFrac(other))
        else:
            return NotImplemented

    def __mixed_irr(self):
        """
        Was part of simplify.
        Extremely complicated.
        Probably not useful.
        Rest in peace.
        """
        # Do nothing if irrational fraction still in range (-1, 1):
        if abs(irr_prod(self.irr)) >= 1:
            return

        # Otherwise, get a greatest-common radical index:
        net_denom: [int, ] = []
        for dnm in map(lambda ex: ex.denom,
                       self.irr.values()):
            net_denom.extend(dnm)
        net_denom = net_denom

        # Make all irrational factor exponents integers:
        for exp in self.irr.values():
            exp.numer.extend(net_denom)
            exp.simplify()

        # Get the mixed form of the inside fraction:
        numer = reduce(mul, map(
            lambda f, ex: f ** exp.numer_prod(),
            self.irr_numer()))
        denom = reduce(mul, map(
            lambda f, ex: f ** exp.numer_prod(),
            self.irr_denom()))
        mixed = rfrac.factorize(numer // denom)
        numer = numer % denom
        roots = {}
        for factor in set(mixed):
            roots[factor] = mixed.count(factor)
        net_denom.sort(reverse=True)
        # Honestly this is a lost cause. What a pity.


def mono_fraction_tests():
    """ Some small test cases for the MonoFrac class. """
    print('\n==========================================\n'
          'mfrac.py @ mono_fraction_tests: //////////\n')
    d0 = {0: 'hi', 1: 'how are you', 2: 'bye'}
    print(list(filter(lambda key: len(d0[key]) < 5, d0)))
    d1 = d0.copy()
    d1[0] = 'hello'
    print(d0[0], d1[0])
    print('\nmfrac.py @ end of mono_fraction_tests ////\n'
          '==========================================\n')


if __name__ == '__main__':
    mono_fraction_tests()
