import rfrac
import mfrac

RF = rfrac.RationalFrac
MF = mfrac.MonoFrac


class Fraction:
    """
    A real-valued fraction.

    Fields:
    -- terms:   [MF, ] = []     A list of MonoFrac objects.
    """

    def __init__(self, number):
        """
        Can be initialized with a Fraction, a list of items that
        can construct a MonoFrac, or with one of RationalFrac,
        MonoFrac, int, or float. If a list or Fraction is given
        as an argument, assumes that it represents a simplified
        Fraction with MonoFrac typed contents. A list is copied
        by reference.
        """
        self.terms = []
        # Copy construction:
        if isinstance(number, Fraction):
            self.terms = number.terms.copy()

        # Initialized with a list:
        elif isinstance(number, list):
            self.terms = number

        # Construction with a rational-valued fraction:
        elif isinstance(number, (MF, RF, int, float, str)):
            self.terms.append(MF(number))

        # Unexpected argument type:
        else:
            raise TypeError(
               f'{str(number)} invalid. '
               'must initialize with one of:\n'
               'Fraction, list, MonoFrac, '
               'RationalFrac, int, float, str.')

    def simplify(self):
        """ Used to merge MonoFrac items with common irr fields. """
        terms = []
        # Collect the sums of MonoFrac
        # entries with equal irrational parts:
        # TODO: This may have a bug depending on 'not in':
        #  I want to try using a dict from similar irr to a
        #  list of their rational parts.
        for mf in self.terms:
            same_irr = filter(lambda other: mf.cmp_degree(other), self.terms)
            term = sum(same_irr, MF(0))
            if term != 0 and term not in terms:
                terms.append(term)
        self.terms = terms

    def factorize(self):
        """ This may be used in taking fractional powers... """
        # TODO: implement factorize

    """
    Public-use, representation/observer methods:
    """
    def __float__(self):
        return sum(map(MF.__float__, self.terms))

    def __int__(self):
        return int(float(self))

    def __str__(self):
        return '+'.join(map(MF.__str__, self.terms))

    def __repr__(self):
        pass

    """
    Addition, and Subtraction:
    """
    def __add__(self, other):
        fsum = Fraction(self)

        if isinstance(other, Fraction):
            fsum.terms.extend(other.terms)

        elif isinstance(other, (MF, RF, int, float)):
            # TODO: perhaps move simplify to first condition
            #  and perform cmp_degree here instead. Same at iadd.
            fsum.terms.append(MF(other))
        else:
            return NotImplemented

        fsum.simplify()
        return fsum

    def __iadd__(self, other):
        if isinstance(other, Fraction):
            self.terms.extend(other.terms)
        elif isinstance(other, (MF, RF, int, float)):
            self.terms.append(MF(other))
        else:
            return NotImplemented
        self.simplify()
        return self

    def __sub__(self, other):
        fsum = Fraction(self)

        if isinstance(other, Fraction):
            fsum.terms.extend([mf.__neg__() for mf in other.terms])
        elif isinstance(other, (MF, RF, int, float)):
            fsum.terms.append(MF(other).__neg__())
        else:
            return NotImplemented

        fsum.simplify()
        return fsum

    def __isub__(self, other):
        if isinstance(other, Fraction):
            self.terms.extend([mf.__neg__() for mf in other.terms])
        elif isinstance(other, (MF, RF, int, float)):
            self.terms.append(MF(other).__neg__())
        else:
            return NotImplemented
        self.simplify()
        return self

    """
    Multiplication, Division, and Exponents:
    """
    def __neg__(self):
        return Fraction([mf.__neg__() for mf in self.terms])

    def __mul__(self, other):
        prod = []
        if isinstance(other, Fraction):
            for t1 in self.terms:
                prod.extend([t1 * t2 for t2 in other.terms])

        elif isinstance(other, (MF, str)):
            f_other = other if isinstance(other, MF) else MF(other)
            prod.extend(mf.__mul__(f_other) for mf in self.terms)

        elif isinstance(other, (RF, int, float, int)):
            f_other = other if isinstance(other, RF) else RF(other)
            prod.extend(mf.__mul__(f_other) for mf in self.terms)
        else:
            return NotImplemented

        prod = Fraction(prod)
        prod.simplify()
        return prod

    def __imul__(self, other):
        pass

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        raise NotImplementedError

    """
    Modulus and powers:
    """
    def __pow__(self, power, modulo=None):
        raise NotImplementedError

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
    m0 = MF(0.125) ** -0.5
    print('sqrt(8):', m0)
    print('1/4:', MF(0.25))
    f0 = Fraction(m0)
    f1 = Fraction(MF(0.25))
    f2 = f0 + f1
    print(f2.terms)
    print(f2, 'x2 =', 2 * f2)
    print(f2 * f2)
    print('\nrfrac.py @ end of fraction_tests /////////\n'
          '==========================================\n')


if __name__ == '__main__':
    fraction_tests()
