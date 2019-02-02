from functools import reduce
from math import sqrt, pi, ceil, cos, sin
from numbers import Number

from fraction import RationalFrac


class Matrix(list):
    """
    A matrix. A list of equal-length columns.
    """
    nrows: int
    ncols: int

    def __init__(self, rows: [[], ]):
        """
        Requires that all elements of m
        are lists of equal length.
        """
        self.nrows = len(rows)
        self.ncols = len(rows[0])
        super().__init__([Vector(row) for row in rows])

    # def __setitem__(self, key, value):
    #     raise PermissionError(
    #         'Matrix does not support row assignment.')

    def is_square(self):
        return self.nrows == self.ncols

    def __add__(self, other):
        """
        Requires that all respective elements of self
        and other are instances of the same type.
        """
        # check if matrix addition is valid
        if isinstance(other, Matrix):
            if not (other.nrows == self.nrows and
                    other.ncols == self.ncols):
                raise MatrixSizeError('dimensions not equal')
            sum_mtx = []
            for r in range(self.nrows):
                sum_mtx.append(
                    [self[r][c] + other[r][c]
                     for c in range(self.ncols)]
                )
            return Matrix(sum_mtx)
        else:
            return NotImplemented

    def __iadd__(self, other):
        """
        Requires that all respective elements of self
        and other are instances of the same type.
        """
        # check if matrix addition is valid
        if isinstance(other, Matrix):
            if not (other.nrows == self.nrows and
                    other.ncols == self.ncols):
                raise MatrixSizeError('dimensions not equal')
            for r in range(self.nrows):
                for c in range(self.ncols):
                    self[r][c] += other[r][c]
        else:
            return NotImplemented

    """
    Special Matrix operations:
    """
    def transpose(self):
        """ Reflection of entries along the main diagonal. """
        t = []
        for c in range(self.ncols):
            t.append([self[r][c] for r in
                      range(self.nrows)])
        return Matrix(t)

    def reduce(self):
        """
        Returns the reduced form of self
        """
        red = Matrix(self)
        free_vars = 0
        for i in range(self.nrows):
            # Find a row where the target col is not zero:
            if float(red[i][i + free_vars]) is 0.0:
                _i = i + 1
                while (_i < self.nrows and
                       float(red[_i][i + free_vars]) is 0.0):
                    _i += 1
                if _i is self.nrows:
                    free_vars += 1
                    continue
                # Switch this row with one
                # where target col is not zero:
                temp = red[i]
                red[i] = red[_i]
                red[_i] = temp

            red[i] *= red[i][i + free_vars].reciprocal()
            for row in self[i+1:]:
                row += -row[i + free_vars] * self[i]

    def det(self) -> (RationalFrac, None):
        """ Returns the determinant of this matrix if it is square. """
        if self.is_square():
            rows = list(range(self.nrows))
            cols = list(range(self.ncols))
            return self.recursive_det(rows, cols)
            # or alternatively, return reduce(mul,
            # [self[i][i] for i in range(self.nrows)])
        else:
            raise MatrixSizeError(
                'cannot take determinant: matrix not square.')

    def recursive_det(self, rows: [int, ], cols: [int, ]) -> RationalFrac:
        """
        Private helper for det(). Recursive function.
        cols and rows are chopped up index slices.
        """
        # Terminating condition:
        if len(rows) is 1:
            # this implies len(cols) is also 1.
            return self[rows[0]][cols[0]]
        else:
            sign = RationalFrac(1)
            det = RationalFrac(0)
            for col in cols:
                _cols = cols.copy()
                _cols.remove(col)
                sub_sum = (sign * self[rows[0]][col] *
                           self.recursive_det(rows[1:], _cols))
                print(rows[0], col, rows[1:], _cols, ':', sign, sub_sum, type(sub_sum))
                det += sub_sum
                sign = -sign
            return det

    def inverse(self):
        """ Finds a matrix A^-1 such that A * A^-1 is I. """
        if not self.is_square():
            raise MatrixSizeError(
                'cannot invert a non-square matrix.')
        elif self.det() is 0:
            raise ArithmeticError(
                'matrix not homogeneous. cannot compute inverse.')

        pass  # TODO

    """
    Matrix multiplication and Scalar multiplication:
    """
    def __matmul__(self, other):
        """
        Returns the matrix multiplication of
        self and other, if it is valid.
        (Ie. a matrix if other is a matrix,
             a vector if other is a vector.
        """
        # Matrix multiplied be another matrix:
        if isinstance(other, Matrix):
            if self.ncols is not other.nrows:
                raise MatrixSizeError('op1 #cols != op2 #rows')
            prod = []
            other_t = other.transpose()
            for r in range(self.nrows):
                prod.append(
                    [reduce(lambda x, y: x + y, self[r].dot(c))
                     for c in other_t]
                )
            return Matrix(prod)

        # Matrix multiplied by a vector:
        elif isinstance(other, Vector):
            if self.ncols is not len(other):
                raise MatrixSizeError('op1 #cols != op2 length')
            return Vector([
                sum(self[r].dot(other))
                for r in range(self.nrows)
            ])

        # Operand 2 is a scalar:
        elif isinstance(other, (RationalFrac, Number)):
            return self.__rmul__(other)

        # Unexpected second operand:
        else:
            return NotImplemented

    def __rmul__(self, other):
        """
        Multiplies this matrix by a leading scalar.
        Returns the product.
        """
        if isinstance(other, (RationalFrac, Number)):
            prod = []
            # Multiply each vector-row by the scalar
            for r in range(self.nrows):
                prod.append(self[r].__rmul__(other))
            return Matrix(prod)
        else:
            return NotImplemented

    def __str__(self):
        s = ''
        contents = []
        for vec in self:
            contents.extend(vec)
        width = max(map(lambda frac: len(str(frac)), contents))

        for row in self:
            rs = ', '.join(map(
                lambda f: f.__str__().center(width), row))
            s += '[%s]\n' % rs
        return s

    @staticmethod
    def identity(n: int):
        """ Returns an n x n identity matrix. """
        im = Matrix.zeros(n)
        for i in range(n):
            im[i][i] = 1
        return im

    @staticmethod
    def ones(n: int):
        """ Returns an n x n matrix of all ones. """
        return Matrix([[RationalFrac(1)] * n] * n)

    @staticmethod
    def zeros(n: int):
        """ Returns an n x n matrix of all zeros. """
        return Matrix([[RationalFrac(0)] * n] * n)


class MatrixSizeError(Exception):
    """
    Used to raise Arithmetic exceptions when
    operand matrix sizes are incompatible.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


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
        are Numbers. Initialize self with
        the fraction versions of v's entries.
        """
        vec = [RationalFrac(n) for n in v]
        super().__init__(vec)

    def __setitem__(self, key, value):
        super().__setitem__(key, RationalFrac(value))

    def __add__(self, other):
        if isinstance(other, (Vector, list, tuple)):
            if len(self) is not len(other):
                raise MatrixSizeError(
                    'cannot add vectors: unequal lengths.')
            else:
                return Vector([
                    self[i] + other[i]
                    for i in range(len(self))
                ])
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Vector):
            if len(self) is not len(other):
                raise MatrixSizeError(
                    'cannot add vectors: unequal lengths.')
            else:
                for i in range(len(self)):
                    self[i] = self[i] + other
        else:
            return NotImplemented

    def __radd__(self, other):
        if isinstance(other, list):
            return self.__add__(other)

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
                '': Matrix([[cos(theta), -sin(theta)],
                            [sin(theta), cos(theta)]])
            },
            3: {
                'x': Matrix([[1, 0, 0],
                             [0, cos(theta), -sin(theta)],
                             [0, sin(theta), cos(theta)]]),
                'y': Matrix([[cos(theta), 0, sin(theta)],
                             [0, 1, 0],
                             [-sin(theta), 0, cos(theta)]]),
                'z': Matrix([[cos(theta), -sin(theta), 0],
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
        return Matrix(self)

    def dot(self, other):
        """
        If the vectors are of equal vector length,
        Returns the dot product of this and other.
        """
        if (isinstance(other, Vector) and
                len(self) is len(other)):
            prod = [self[i] * other[i] for i in range(len(self))]
            return Vector(prod)
        else:
            raise MatrixSizeError('vector lengths incompatible.')

    def __mul__(self, *others):
        """ Vector cross product. """
        # TODO: reconsider *others: not suited for parsing user expressions.
        if len(others) != len(self) - 2:
            raise MatrixSizeError(
                'not enough lists/vectors to perform cross-product.')
        elif any(map(lambda v: len(v) != len(self), others)):
            raise MatrixSizeError(
                'the other lists/vectors are not all of equal length.')

        # Inputs verified as valid. setup matrix:
        mtx = [[1 if i % 2 is 0 else -1
                for i in range(len(self))],
               self]
        for other in others:
            mtx.append(other)
        mtx = Matrix(mtx)

        # Calculate the cross product:
        cross = []
        rows = list(range(1, mtx.nrows))
        cols = list(range(len(self)))
        for c in cols:
            _cols = cols.copy()
            _cols.remove(c)
            cross.append(mtx[0][c] * mtx.recursive_det(rows, _cols))
        return Vector(cross)

    def __rmul__(self, other):
        """ Scalar multiplication. """
        if isinstance(other, RationalFrac):
            return Vector([
                other * entry for entry in self
            ])
        elif isinstance(other, Number):
            f_other = RationalFrac(other)
            return Vector([
                f_other * entry for entry in self
            ])
        else:
            return NotImplemented


# Small tests:
vec1 = Vector([0, 0.5, 2])
mtx1 = Matrix([[0, 4.5],  # [0, 11]
               [2, 3]])   # [2,  3]
frac1 = RationalFrac(1)
# print(frac1)
# print(frac1 ** -2)
# print(frac1, frac1.numer, frac1.denom)
# print(vec1)
# print(5 * vec1)
# print(mtx1)
# print(mtx1 @ mtx1)
# print(2 * mtx1)
# print(2 * mtx1 @ mtx1)
# TODO: Test vector cross method.
# print((2 * mtx1 @ mtx1).det(), 'is ', 18 * 36 - 27 * 12, '?')
i5 = Matrix.identity(5)
square3 = Matrix([
    [-2, 2, -3],
    [-1, 1, 3],
    [2, 0, -1]
])
print(square3)
print(square3.det(), 'vs 18')
# print(i5)
i5[0][0] = RationalFrac(2)
# print(i5)
print(vec1)
# print(vec1 * vec1)
# print([0, 1, 0] + vec1)
