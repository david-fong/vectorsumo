from functools import reduce
from numbers import Number

import rfrac
from vector import Vector

RF = rfrac.RationalFrac


class MatrixSizeError(Exception):
    """
    Used to raise Arithmetic exceptions when
    operand matrix sizes are incompatible.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Matrix(list):
    """
    A matrix. A list of equal-length columns.
    """
    nrows: int
    ncols: int

    def __init__(self, rows: [[], ]):
        """
        Requires that all elements of m
        are lists or Vector objects of equal length.
        """
        self.nrows = len(rows)
        self.ncols = len(rows[0])
        super().__init__([Vector(row) for row in rows])

    def __str__(self):
        s = ''
        contents = []
        for vec in self:
            contents.extend(vec)
        width = max(map(lambda frac: len(str(frac)), contents))
        if all(map(lambda frac: str(frac).startswith(' '), contents)):
            for row in self:
                rs = ', '.join(map(
                    lambda f: f.__str__().lstrip()
                               .center(width - 1), row))
                s += '[%s]\n' % rs
        else:
            for row in self:
                rs = ', '.join(map(
                    lambda f: f.__str__().center(width), row))
                s += '[%s]\n' % rs
        return s

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
            if float(red[i][i + free_vars]) == 0.0:
                _i = i + 1
                while (_i < self.nrows and
                       float(red[_i][i + free_vars]) == 0.0):
                    _i += 1
                if _i == self.nrows:
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

    def det(self) -> (RF, None):
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

    def recursive_det(self, rows: [int, ], cols: [int, ]) -> RF:
        """
        Private helper for det(). Recursive function.
        cols and rows are chopped up index slices.
        """
        # Terminating condition:
        if len(rows) == 1:
            # this implies len(cols) is also 1.
            return self[rows[0]][cols[0]]
        else:
            sign = RF(1)
            det = RF(0)
            for col in cols:
                _cols = cols.copy()
                _cols.remove(col)
                sub_sub_det = self.recursive_det(rows[1:], _cols)
                sub_det = sign * self[rows[0]][col] * sub_sub_det

                # print(rows[0], col, rows[1:], _cols, ':',
                #       self[rows[0]][col], sub_sub_det, sub_det, sub_det.denom)
                det += sub_det
                sign = -sign
            return det

    def inverse(self):
        """ Finds a matrix A^-1 such that A * A^-1 is I. """
        if not self.is_square():
            raise MatrixSizeError(
                'cannot invert a non-square matrix.')
        elif self.det() == 0:
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
            if self.ncols != other.nrows:
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
            if self.ncols != len(other):
                raise MatrixSizeError('op1 #cols != op2 length')
            return Vector([
                sum(self[r].dot(other))
                for r in range(self.nrows)
            ])

        # Operand 2 is a scalar:
        elif isinstance(other, (RF, Number)):
            return self.__rmul__(other)

        # Unexpected second operand:
        else:
            return NotImplemented

    def __rmul__(self, other):
        """
        Multiplies this matrix by a leading scalar.
        Returns the product.
        """
        if isinstance(other, (RF, Number)):
            prod = []
            # Multiply each vector-row by the scalar
            for r in range(self.nrows):
                prod.append(self[r].__rmul__(other))
            return Matrix(prod)
        else:
            return NotImplemented

    def __eq__(self, other):
        """
        Checks if all corresponding pairs
        of Vectors are equal using __eq__().
        """
        if not isinstance(other, Matrix):
            return False
        elif not (self.nrows == other.nrows and
                  self.ncols == other.ncols):
            return False
        else:
            return all(map(
                lambda i: self[i].__eq__(other[i]),
                list(range(self.nrows))
            ))

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
        return Matrix([[RF(1)] * n] * n)

    @staticmethod
    def zeros(n: int):
        """ Returns an n x n matrix of all zeros. """
        return Matrix([[RF(0)] * n] * n)


def matrix_tests():
    print('\n==========================================')
    print('matrix.py @ matrix_tests: ////////////////\n')
    frac1 = RF(0.125)
    # print(frac1)
    vec1 = Vector([0, 0.5, 2])
    mtx1 = Matrix([[0, 4.5],  # [0, 11]
                   [2, 3]])  # [2,  3]
    RF(-0)
    # print(frac1 ** -2)
    # print(vec1)
    # print(5 * vec1)
    print(mtx1)
    print(mtx1 @ mtx1)
    # print(2 * mtx1)
    # print(2 * mtx1 @ mtx1)
    # TODO: Test vector cross method.
    # print((2 * mtx1 @ mtx1).det(), 'is ', 18 * 36 - 27 * 12, '?')
    i5 = Matrix.identity(5)
    square3_0 = Matrix([
        [-2, 2, -3],
        [-1, 1, 3],
        [2, 0, -1]
    ])
    square3_1 = Matrix([
        [1, 2, 4],
        [-1, 3, 0],
        [4, 1, 0]
    ])
    print(square3_0)
    print('actual =', square3_0.det(), 'and expected = 18')
    print(square3_1)
    print('actual =', square3_1.det(), 'and expected = -52')
    # print(i5)
    # i5[0][0] = frac1
    # frac1 *= 2
    # i5[0] *= 2
    # print(i5, frac1)
    print(vec1)
    # print(vec1 * vec1)
    # print([0, 1, 0] + vec1)
    print('\nmatrix.py @ end of matrix_tests //////////')
    print('==========================================\n')


if __name__ == '__main__':
    matrix_tests()
