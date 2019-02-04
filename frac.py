import rfrac
import mfrac

RF = rfrac.RationalFrac
MF = mfrac.MonoFrac


class Fraction(list):
    """
    A real-valued fraction.

    A list of MonoFrac objects.
    """

    def __init__(self, number):
        """
        If initialized with a list, assumes the list
        contains only MonoFrac type objects.
        """
        # Copy construction:
        if isinstance(number, (Fraction, list)):
            self.neg = bool(number.neg)
            super(Fraction, self).__init__(number)

        # Construction with a rational-valued fraction:
        elif isinstance(number, (RF, int, float)):
            super(Fraction, self).__init__([RF(number), ])

        # Unexpected argument type:
        else:
            raise TypeError(
                str(number) + ' invalid. must initialize with one of:\n'
                'Fraction, RationalFrac, int, float.')

    def simplify(self):
        """ Used to merge MonoFrac items with common irr fields. """
        common_irr = dict.fromkeys(
            map(lambda mono: mono.irr, self), MF(0)
        )
        for mf in self:
            common_irr[mf.irr] += mf.rational
        self.clear()
        for irr, rational in common_irr:
            self.append(MF(rational, irr))

    """
    Public-use, representation/observer methods:
    """
    def __float__(self):
        return sum(map(MF.__float__, self))

    def __int__(self):
        return int(float(self))

    def __str__(self):
        return '+'.join(map(lambda mf: mf.__str__(), self))

    def __repr__(self):
        pass

    """
    Negation, Addition, and Subtraction:
    """
    def __neg__(self):
        return Fraction([mf.__neg__() for mf in self])

    def __add__(self, other):
        fsum = Fraction(super(Fraction, self).__add__(other))
        fsum.simplify()
        return fsum

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
    print('\n==========================================\n'
          'rfrac.py @ fraction_tests: ///////////////\n')
    f0 = Fraction()
    print('\nrfrac.py @ end of fraction_tests /////////\n'
          '==========================================\n')


if __name__ == '__main__':
    fraction_tests()
