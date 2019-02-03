from functools import reduce
from operator import mul

import rfrac


RF = rfrac.RationalFrac


class Fraction(dict):
    """
    A real-valued fraction.

    Consists of a single dict from prime factors(int),
    to their powers, which are RationalFrac objects.

    Special cases: When zero, self.has_key(0) is True.
                   When undef, self[0].neg is True.
    """
    neg = False

    def __init__(self, number):
        """
        Must be initialized with a rational fraction
        or another Fraction object.
        """
        # Copy construction:
        if isinstance(number, Fraction):
            self.neg = bool(number.neg)
            super().__init__(number)

        # Construction with a rational-valued
        elif isinstance(number, (RF, int, float)):
            rf = RF(number)
            self.neg = bool(rf.neg)
            factors: dict = {}
            for fac in rf.numer:
                factors[fac] = RF(rf.numer.count(fac))
            for fac in rf.denom:
                factors[fac] = RF(rf.denom.count(fac).__neg__())
            super().__init__(factors)

        # Unexpected argument type:
        else:
            raise TypeError(
                str(number) + 'invalid. \n' +
                'must initialize with one of: \n' +
                'Fraction, RationalFrac, int, float.')

    """
    Public-use, representation/observer methods:
    """
    def __getitem__(self, factor):
        """
        Gets the power of factor,
        or the RationalFrac if
        factor is not in self.
        """
        return self.get(factor, RF(0))

    def __setitem__(self, key, value):


    def __float__(self):
        pass

    def __int__(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def numer_prod(self):
        # TODO: decide on what I want to return here.
        #  Maybe a Fraction with positive exp values?
        #  Then denom_prod would do something like
        #   "self.reciprocal.numer_prod()".
        numer = filter(lambda fac, exp: not exp.neg, self.items())
        return reduce(mul, map(lambda fac, exp: fac.__pow__(exp), numer))

    def denom_prod(self):
        pass

    """
    Negation, Addition, and Subtraction:
    """
    def __neg__(self):
        negated = self.copy()
        negated.neg = not self.neg
        return negated

    def __add__(self, other):
        # TODO: This will be tricky...
        #  not sure what to do yet...
        #  I think might need to use 0-degree
        #      polynomials as expressions...
        #  I thought I was so clever with this representation :|
        pass

    def __radd__(self, other):
        pass

    def __sub__(self, other):
        pass

    def reciprocal(self):
        pass

    """
    Multiplication, Division, and Exponents:
    """
    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __pow__(self, power, modulo=None):
        pass

    """
    Rich comparison methods:
    """
    def __eq__(self, other):
        pass

    def __lt__(self, other):
        pass


def fraction_tests():
    """ Some small test cases for the Fraction class. """
    print('\n==========================================')
    print('rfrac.py @ fraction_tests: ////////////\n')
    d0 = {0: 'hi'}
    d1 = dict(d0)
    d1[0] = 'hello'
    d1.get(0) =
    print(d0[0], d1[0])
    print('\nrfrac.py @ end of fraction_tests //////')
    print('==========================================\n')


if __name__ == '__main__':
    fraction_tests()
