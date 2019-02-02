import rfrac


RF = rfrac.RationalFrac


class Fraction(dict):
    """
    A real-valued fraction.

    Consists of a single dict from prime factors(int),
    to their powers, which are RationalFrac objects.

    Special cases: When zero, self[0] > 0 and len(self) == 1.
                   When undef, self[0] < 0.
    """
    neg = False

    def __init__(self, number):
        """ Must be initialized with a rational fraction. """
        if not isinstance(number, (Fraction, RF, int, float)):
            raise TypeError(str(number) + 'invalid. \n' +
                            'must initialize with one of: \n' +
                            'Fraction, RationalFrac, int, float.')
        rf = RF(number)
        self.neg = bool(rf.neg)
        factors: dict = {}
        for fac in rf.numer:
            factors[fac] = RF(rf.numer.count(fac))
        for fac in rf.denom:
            factors[fac] = RF(rf.denom.count(fac).__neg__())
        super().__init__(factors)

    def simplify(self):
        pass  # TODO:

    """
    Public-use, representation/observer methods:
    """
    def __getitem__(self, item):
        if item not in self.keys():
            pass

    def __float__(self):
        pass

    def __int__(self):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def numer_prod(self):
        pass

    def denom_prod(self):
        pass

    """
    Negation, Addition, and Subtraction:
    """
    def __neg__(self):
        pass

    def __add__(self, other):
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

    print('\nrfrac.py @ end of fraction_tests //////')
    print('==========================================\n')


if __name__ == '__main__':
    fraction_tests()
