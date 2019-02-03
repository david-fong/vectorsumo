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
    A fraction permitting factors to RationalFrac valued powers,
    but with the unchecked constraint on addition and subtraction
    that the irrational parts of each operand must be the same.
    Designed for use in the Fraction class.

    Represented as a RationalFrac and a dict from prime factors to
    their powers, which are also RationalFrac objects. This dict
    represents the irrational part of the fraction. its value is
    maintained by a simplification operation such that none of its
    factors' exponents have equivalent integer values.

    Special cases:
    If all of the factors of the fraction represented by this
    MonoFrac object have integer exponents, its irr field will be
    an empty dictionary. This includes when the fraction is 0.
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
            self.rational = number.rational.__copy__()
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

    def __copy__(self):
        """ Returns a copy of this MonoFrac object. """
        copy = MonoFrac(0)
        copy.rational = self.rational.__copy__()
        copy.irr = self.irr.copy()
        return copy

    def simplify(self):
        for fac, exp in self.irr.items():
            # fac ** 0 == 1. Remove redundant mapping:
            if 0 in exp.numer:
                del self.irr[fac]

            # Factor out any rational parts
            # of self.irr to self.rational:
            elif len(exp.denom) is 0:
                rational = [fac, ] * exp.numer_prod()
                if exp.neg:
                    self.rational.denom.extend(rational)
                else:
                    self.rational.numer.extend(rational)
                del self.irr[fac]

    """
    Public-use, representation/observer methods:
    """
    def cmp_degree(self, other):
        """
        Must be used externally to check if this
        MonoFrac object can be added with other.

        Returns whether the irrational parts of
        self and other are the same.
        """
        if isinstance(other, MonoFrac):
            return self.irr == other.irr

        # If other has no irrational part:
        elif isinstance(other, (RF, int, float)):
            return len(self.irr) == 0
        else:
            raise TypeError(
                'can only compare degrees with '
                'another MonoFrac object.')

    def __float__(self) -> float:
        return float(self.rational) * irr_prod(self.irr)

    def __int__(self) -> int:
        return int(self.__float__())

    def __str__(self):
        pass

    def __repr__(self):
        pass

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

    """
    Addition and Subtraction:
    """
    def __add__(self, other):
        """
        Returns the sum of this MonoFrac to other
        as a MonoFrac. If other is also a MonoFrac,
        assumes that self.cmp_degree(other) is True.
        """
        if isinstance(other, MonoFrac):
            fsum = self.__copy__()
            fsum.rational += other.rational
            return fsum
        elif isinstance(other, RF):
            fsum = self.__copy__()
            fsum.rational += other
            return fsum
        elif isinstance(other, (int, float)):
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
            self.__iadd__(MonoFrac(other))
            return self
        else:
            return NotImplemented

    def __sub__(self, other):
        """
        Returns the difference between this MonoFrac
        and other as a MonoFrac. If other is also a
        MonoFrac, assumes that self.cmp_degree(other)
        is True.
        """
        return self.__iadd__(-other)

    """
    Multiplication, Division, and Exponents:
    """
    def reciprocal(self):
        recip = MonoFrac(self.rational.reciprocal())
        recip.irr = {}
        for fac in self.irr.keys():
            recip.irr[fac] = self.irr[fac].__neg__()
        return recip

    def __neg__(self):
        """ Returns the negative version of self. """
        negated = self.__copy__()
        negated.rational.neg = not self.rational.neg

    def __mul__(self, other):
        """ Returns the product of this and another number. """
        # Multiplication by another MonoFrac:
        if isinstance(other, MonoFrac):
            prod = self.__copy__()
            prod.rational *= other.rational

            # Factor in irrational factors from both self and other:
            for fac, exp in other.irr.items():
                if fac in prod.irr:
                    prod.irr[fac] += exp
                else:
                    prod.irr[fac] = exp.__copy__()
            prod.simplify()
            return prod

        # Multiplication by a RationalFrac, int, or float:
        elif isinstance(other, (RF, int, float)):
            prod = self.__copy__()
            prod.rational *= other
            return prod

        else:
            return NotImplemented

    def __imul__(self, other):
        """ Multiplies self by other in-place. """
        # Multiplication by another MonoFrac:
        if isinstance(other, MonoFrac):
            self.rational *= other.rational

            # Factor in irrational factors from both self and other:
            for fac, exp in other.irr.items():
                if fac in self.irr:
                    self.irr[fac] += exp
                else:
                    self.irr[fac] = exp.__copy__()
            self.simplify()
            return self

        # Multiplication by a RationalFrac, int, or float:
        elif isinstance(other, (RF, int, float)):
            self.rational *= other
            return self

        else:
            return NotImplemented

    def __rmul__(self, other):
        """ Returns the product of this and a number. """
        pass  # TODO:

    def __truediv__(self, other):
        """ Returns the quotient of this and another fraction. """
        # Division by another MonoFrac:
        if isinstance(other, MonoFrac):
            quot = self.__copy__()
            quot.rational /= other.rational

            # Factor in irrational factors from both self and other:
            for fac, exp in other.irr.items():
                if fac in quot.irr:
                    quot.irr[fac] -= exp
                else:
                    quot.irr[fac] = -exp.__copy__()
            quot.simplify()
            return quot

        # Division by a RationalFrac, int, or float:
        elif isinstance(other, (RF, int, float)):
            quot = self.__copy__()
            quot.rational /= other
            return quot

        else:
            return NotImplemented

    def __pow__(self, power, modulo=None):
        """ Returns this fraction to the specified power. """
        # If power is an int:
        if isinstance(power, int):
            power = self.__copy__()
            power.rational **= power

        # If power is a RationalFrac:
        elif isinstance(power, (RF, float)):
            power = MonoFrac(1)
            # Move rational numerator to irrational dict:
            for fac in self.rational.numer:
                if fac in self.irr:
                    power.irr[fac] += 1
                else:
                    power.irr[fac] = 1
            # Move rational denominator to irrational dict:
            for fac in self.rational.denom:
                if fac in self.irr:
                    power.irr[fac] += 1
                else:
                    power.irr[fac] = -1
        else:
            return NotImplemented

        # Use mathematical power rules on irrational part:
        for fac in power.irr.keys():
            power.irr[fac] *= power
        power.simplify()
        return power

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
    for k, v in d0.items():
        d0[k] = 'hiya'
    print(d0[0], d1[0])
    print('\nmfrac.py @ end of mono_fraction_tests ////\n'
          '==========================================\n')


if __name__ == '__main__':
    mono_fraction_tests()