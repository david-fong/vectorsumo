from math import ceil, pi, cos, sin, sqrt

import matrix
import rfrac


RF = rfrac.RationalFrac


class Vector(list):
    """
    A vector. All entries are Fraction objects.
    """
    # TODO: once Fraction class is done,
    #  refactor to use it instead of RationalFrac
    #  Also refactor corresponding parts of Matrix class.

    def __init__(self, v: list):
        """
        Requires that all elements of v
        are can initialize RationalFrac objects.

        IMPORTANT: Does not initialize with copies
        of RationalFrac instances where provided.
        External changes will be reflected in
        the corresponding entries of THIS matrix.
        """
        vec = [n if isinstance(n, RF)
               else RF(n) for n in v]
        super().__init__(vec)

    def __setitem__(self, key, value):
        """ Performs type-checking and appropriate conversions. """
        if isinstance(value, RF):
            super().__setitem__(key, value)
        elif isinstance(value, (int, float, str)):
            super().__setitem__(key, RF(value))
        else:
            raise TypeError(
                f'{type(value)} invalid.\n'
                'can only set int, float, or \n'
                'RationalFrac type objects in Vector.')

    def append(self, obj):
        super(Vector, self).append(RF(obj))

    def extend(self, iterable):
        super(Vector, self).extend([RF(obj) for obj in iterable])

    def __add__(self, other):
        if isinstance(other, (Vector, list, tuple)):
            if len(self) == len(other):
                return Vector([
                    self[i] + other[i]
                    for i in range(len(self))
                ])
            else:
                raise matrix.MatrixSizeError(
                    'cannot add vectors of unequal lengths.')
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Vector):
            if len(self) == len(other):
                for i in range(len(self)):
                    self[i] += other[i]
                return self
            else:
                raise matrix.MatrixSizeError(
                    'cannot add vectors of unequal lengths.')
        else:
            return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __isub__(self, other):
        """ Subtracts entries of other from entries of self in place. """
        if isinstance(other, (list, tuple, Vector)):
            if len(other) == len(self):
                for i in range(len(self)):
                    self[i] -= other[i]
                return self
            else:
                raise matrix.MatrixSizeError(
                    'cannot subtract vectors of unequal lengths.')
        else:
            return NotImplemented

    def norm(self):
        """ Returns the 'length' of the vector. """
        # Equivalent to sqrt(sum(self.dot(self))):
        return sqrt(sum(map(lambda x: x ** 2, self)))

    @staticmethod
    def rot_matrix(theta: float, size: int, axis: str):
        """ Returns a rotation matrix """
        # TODO: This sucks. When monomials and functions are implemented,
        #  support them in matrices and call something
        #  like: " rm[size][axis].eval({'o': o}) "
        rm = {
            2: {
                '': matrix.Matrix([[cos(theta), -sin(theta)],
                                   [sin(theta), cos(theta)]])
            },
            3: {
                'x': matrix.Matrix([[1, 0, 0],
                                    [0, cos(theta), -sin(theta)],
                                    [0, sin(theta), cos(theta)]]),
                'y': matrix.Matrix([[cos(theta), 0, sin(theta)],
                                    [0, 1, 0],
                                    [-sin(theta), 0, cos(theta)]]),
                'z': matrix.Matrix([[cos(theta), -sin(theta), 0],
                                    [sin(theta), cos(theta), 0],
                                    [0, 0, 1]])
            }
        }  # Rotation matrices based on size
        return rm[size][axis]

    def rot(self, o, axis=''):
        """
        Returns a rotated view of a vector in space.
        The rotation is counterclockwise by theta,
        about the specified axis when relevant.
        """
        if o < 0:
            o = ceil(-o / 2 / pi) * 2 * pi + o
        o %= 2 * pi
        return Vector.rot_matrix(0, len(self), axis) @ self

    def transform(self):
        """Return a [1 x len(self)] matrix"""
        return matrix.Matrix(self)

    def dot(self, other):
        """
        If the vectors are of equal vector length,
        Returns the dot product of this and other.
        """
        if (isinstance(other, Vector) and
                len(self) == len(other)):
            prod = [self[i] * other[i] for i in range(len(self))]
            return Vector(prod)
        else:
            raise matrix.MatrixSizeError('vector lengths incompatible.')

    def __neg__(self):
        """
        Returns a copy of self where each entry's
        sign is its original's flipped version.
        """
        return Vector([-num for num in self])

    def __matmul__(self, *others):
        """ Vector cross product. """
        # TODO: reconsider *others:
        #  not suited for parsing user expressions.
        if len(others) != len(self) - 2:
            raise matrix.MatrixSizeError(
                'not enough lists/vectors to perform cross-product.')
        elif any(map(lambda v: len(v) != len(self), others)):
            raise matrix.MatrixSizeError(
                'the other lists/vectors are not all of equal length.')

        # Inputs verified as valid. setup matrix:
        mtx = [[1 if i % 2 == 0 else -1
                for i in range(len(self))],
               self]
        for other in others:
            mtx.append(other)
        mtx = matrix.Matrix(mtx)

        # Calculate the cross product:
        cross = []
        rows = list(range(1, mtx.nrows))
        cols = list(range(len(self)))
        for c in cols:
            _cols = cols.copy()
            _cols.remove(c)
            cross.append(mtx[0][c] * mtx.recursive_det(rows, _cols))
        return Vector(cross)

    def __mul__(self, other):
        """ Scalar multiplication. """
        if isinstance(other, RF):
            return Vector([
                other * entry for entry in self
            ])
        elif isinstance(other, (int, float)):
            f_other = RF(other)
            return Vector([
                f_other * entry for entry in self
            ])
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        """
        Checks if all corresponding pairs of
        elements are equal using __eq__().
        """
        if not isinstance(other, Vector):
            return False
        elif len(self) != len(other):
            return False
        else:
            return all(map(
                # Delegates to entry-type content equality comparison:
                lambda i: self[i] == other[i],
                list(range(len(self)))
            ))


def vector_tests():
    print('\n==========================================\n'
          'vector.py @ vector_tests: ////////////////\n')
    vec1 = Vector([0, 0.5, 2])
    print(vec1)
    print(vec1 @ vec1)
    print([0, 1, RF(5, 7)] + vec1)

    vec1 -= [1, 1, 1]
    print('in place subtraction test:', vec1)
    print('neg test:', -vec1)
    vec1 *= 2.5
    print('in place multiplication test:', vec1)
    print('\nvector.py @ end of vector_tests //////////\n'
          '==========================================\n')


if __name__ == '__main__':
    vector_tests()
