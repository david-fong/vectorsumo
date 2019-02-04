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
        Can be initialized with a Fraction,
        a list of items that can construct a MonoFrac,
        or with a RationalFrac, MonoFrac, int, or float.
        """
        # Copy construction:
        if isinstance(number, Fraction):
            super(Fraction, self).__init__(number)

        # Initialized with a list:
        elif isinstance(number, list):
            mono_fracs = [
                num if isinstance(num, MF)
                else MF(num)
                for num in number]
            super(Fraction, self).__init__(mono_fracs)

        # Construction with a rational-valued fraction:
        elif isinstance(number, (RF, MF, int, float)):
            super(Fraction, self).__init__([MF(number), ])

        # Unexpected argument type:
        else:
            raise TypeError(
               f'{str(number)} invalid. must initialize with one of:\n'
               'Fraction, RationalFrac, int, float.')

    def copy(self):
        copy =

    def simplify(self):
        """ Used to merge MonoFrac items with common irr fields. """
        terms = []
        for mf in self:
            # Collect the sums of MonoFrac entries with equal irrational parts:
            same_irr = filter(lambda other: mf.cmp_degree(other), self)
            term = sum(same_irr, MF(0))
            if term != 0:
                terms.append(term)

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
        if isinstance(other, Fraction):
            fsum = self.copy()
            fsum.extend(other)
            fsum.simplify()
            return fsum
        elif isinstance(other, (MF, RF, int, float)):
            fsum = Fraction(self.append(MF(other)))
            fsum.simplify()
            return fsum
        else:
            return NotImplemented

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
    f0 = Fraction(MF(0.125) ** -0.5)
    f1 = Fraction(MF(0.25))
    print(f0)
    print(f0 + f1, f0.extend(f1))
    print('\nrfrac.py @ end of fraction_tests /////////\n'
          '==========================================\n')


if __name__ == '__main__':
    fraction_tests()
