from functools import reduce
from numbers import Number

import rfrac
import vector

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
        super().__init__([vector.Vector(row) for row in rows])

    def append(self, obj):
        """ Assumes that len(obj) == self.ncols. """
        self.nrows += 1
        super(Matrix, self).append(vector.Vector(obj))

    def extend(self, iterable):
        """
        Assumes that len(obj) == self.ncols
        for each obj in iterable.
        """
        rows = [vector.Vector(obj) for obj in iterable]
        self.nrows += len(rows)
        super(Matrix, self).extend(rows)

    def __str__(self):
        contents = []
        for vec in self:
            contents.extend(vec)
        width = max(map(lambda frac: len(frac.__str__()), contents))
        return '\n'.join([
            '[%s]' % ', '.join(
                map(lambda f: f.__str__().center(width), row)
            ) for row in self
        ])

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
        """
        Returns a version of this matrix where all
        entries are reflected along the main diagonal.
        """
        t = []
        for c in range(self.ncols):
            t.append([self[r][c] for r in
                      range(self.nrows)])
        return Matrix(t)

    def add_solution_col(self, solution):
        """
        Appends the solution column to
        the right side of this matrix.
        """
        assert len(solution) == self.nrows
        self.ncols += 1
        for row in range(self.nrows):
            self[row].append(solution[row])

    def rref(self):
        """
        Returns the reduced form of self
        """
        red = Matrix(self)
        free_vars = 0  # Increments when a column is all zeros.

        for r in range(self.nrows):
            # Find a row where the target by the next column is not zero:
            target = r
            while red[target][r + free_vars] == 0:
                target += 1
                if target == self.nrows:
                    free_vars += 1
                    target = r
                    if r + free_vars == self.ncols:
                        return red
            # Put swap target position to get upper triangular form:
            zero_row = red[r]
            red[r] = red[target]
            red[target] = zero_row

            # Perform reduction on other rows by target:
            red[r] *= 1 / red[r][r + free_vars]
            for other_row in red:
                if other_row is not red[r]:
                    anti_target_row = other_row[r + free_vars] * red[r]
                    other_row -= anti_target_row
        return red

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
            sign = 1
            det = 0
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

        # All conditions met. calculate the inverse:
        i = Matrix.identity(self.nrows)
        # TODO:

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
        elif isinstance(other, vector.Vector):
            if self.ncols != len(other):
                raise MatrixSizeError('op1 #cols != op2 length')
            return vector.Vector([
                sum(self[r].dot(other))
                for r in range(self.nrows)
            ])

        # Unexpected second operand:
        else:
            return NotImplemented

    def __mul__(self, other):
        """
        Multiplies this matrix by a leading scalar.
        Returns the product.
        """
        if isinstance(other, (RF, Number)):
            prod = []
            # Multiply each vector-row by the scalar
            for r in range(self.nrows):
                prod.append(self[r] * other)
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
                # Delegates to Vector content equality comparison:
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
    i5 = Matrix.identity(5)
    i5[0][0] = RF(0.125)
    print(i5)

    sqr3_0 = Matrix([[-2, 2, -3], [-1, 1, 3], [2, 0, -1]])
    print(sqr3_0, '\nactual =', sqr3_0.det(), 'and expected = 18\n')

    sqr3_1 = Matrix([[1, 2, 4], [-1, 3, 0], [4, 1, 0]])
    print(sqr3_1, '\nactual =', sqr3_1.det(), 'and expected = -52\n')

    rref_ex = Matrix([[1, 2, 3], [2, -1, 1], [3, 0, -1]])
    rref_soln = [9, 8, 3]
    rref_ex.add_solution_col(rref_soln)
    print(rref_ex)
    print('\nrref =\n', rref_ex.rref())
    print('\nmatrix.py @ end of matrix_tests //////////')
    print('==========================================\n')


if __name__ == '__main__':
    matrix_tests()
