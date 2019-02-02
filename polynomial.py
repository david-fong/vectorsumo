from numbers import Number

from rfrac import RationalFrac


class Monomial(dict):
    """
    The product of a coefficient and several variables.
    Represented as a dictionary from strings, which are
    variable names, to integers, which are their degrees.
    """
    coefficient: RationalFrac

    def __init__(self, coefficient: (Number, RationalFrac), **kwargs: _VT):
        super().__init__(**kwargs)
        self.coefficient = coefficient
        # TODO

    def deg(self):
        return sum(self.values())

    def __lt__(self, other):
        """
        true if self.deg() < other.deg(),
        or if self.deg() is other.deg() and
            self.keys() < other.keys(),
            or otherwise if the corresponding items list is less.
        """
        if isinstance(other, Monomial):
            pass  # TODO
        else:
            return NotImplemented


class Polynomial:
    """
    A collection of polynomials
    """
    terms: [Monomial, ] = []

    def __init__(self):
        pass  # TODO;


# just testing syntax:
monomial_vars = {'x': 2, 'y': 1, 'z': 0}
for entry in monomial_vars.items():
    print(entry)
