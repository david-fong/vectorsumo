from math import sqrt, pi, ceil, cos, sin, log10
from numbers import Number


class Matrix(list):
    """
    A matrix. A list of equal-length columns.
    """
    self: [[Number, ], ]
    nrows: int
    ncols: int

    def __init__(self, columns: [[], ], usrfmt=True):
        """
        Requires that all elements of m
        are lists of equal length.
        """
        self.ncols = len(columns)
        self.nrows = len(columns[0])
        super().__init__(columns)
        if usrfmt:
            t = self.transform()
            self.clear()
            self.extend(t)
            self.ncols = len(columns)
            self.nrows = len(columns[0])

    def is_square(self):
        return self.nrows is self.ncols

    def __iadd__(self, other):
        """
        Requires that all respective elements of self
        and other are instances of the same type.
        """
        # check if matrix addition is valid
        if not isinstance(other, Matrix):
            return NotImplemented
        elif not (other.nrows is self.nrows and
                  other.ncols is self.ncols):
            return
        for c in range(self.ncols):
            for r in range(self.nrows):
                self[c][r] += other[c][r]

    def __add__(self, other):
        """
        Requires that all respective elements of self
        and other are instances of the same type.
        """
        # check if matrix addition is valid
        if not isinstance(other, Matrix):
            return NotImplemented
        elif not (other.nrows is self.nrows and
                  other.ncols is self.ncols):
            return
        sum_mtx = []
        for c in range(self.ncols):
            sum_col = []
            for r in range(self.nrows):
                sum_col.append(self[c][r] + other[c][r])
            sum_mtx.append(sum_col)
        return Matrix(sum_mtx, usrfmt=False)

    def transform(self):
        """
        Reflection of entries along the main diagonal.
        """
        t = []
        for r in range(self.nrows):
            t.append([self[c][r] for c in
                      range(self.ncols)])
        return Matrix(t, usrfmt=False)

    def det(self) -> (Number, None):
        """Returns the determinant of this matrix if it is square."""
        if not self.is_square():
            return
        cols = list(range(self.ncols))
        rows = list(range(self.nrows))
        return self.__det(cols, rows)

    def __det(self, cols: [Number, ], rows: [Number, ]) -> Number:
        """
        Private helper for det(). Recursive function.
        cols and rows are chopped up index slices.
        """
        # Terminating condition:
        if len(cols) is 1:  # implies len(rows) is 1
            return self[cols[0]][rows[0]]
        else:
            det = 0.0
            for i in range(len(cols)):
                _cols = cols.copy()
                _cols.remove(i)
                _det = self[cols[i]][rows[0]]
                _det *= self.__det(_cols, rows[1:])
                if i % 2 is 1:
                    _det *= -1
                det += _det
            return det

    def reduce(self):
        pass  # TODO:

    def inverse(self):
        if not self.is_square():
            return
        pass  # TODO

    def __mul__(self, other):
        """
        Returns the matrix multiplication of
        self and other, if it is valid.
        """
        if (isinstance(other, Matrix) and
                self.ncols is other.nrows):
            prod = []
            for c in range(other.ncols):
                col = []
                for r in range(self.nrows):
                    entry = 0
                    for i in range(self.ncols):
                        entry += self[i][r] * other[c][i]
                    col.append(entry)
                prod.append(col)
            return Matrix(prod, usrfmt=False)
        else:
            return NotImplemented

    def __rmul__(self, other):
        """
        Multiplies this matrix by a leading scalar.
        Returns the product.
        """
        if isinstance(other, Number):
            m = []
            for c in range(self.ncols):
                m.append([e * other for e in self[c]])
            return Matrix(m, usrfmt=False)
        else:
            return NotImplemented

    def __str__(self):
        s = ''
        maximum = max(map(lambda c: max(c), self))
        width = int(ceil(log10(maximum)))

        for row in self.transform():
            rs = ', '.join(map(
                lambda x: ('%1.2f' % x).rjust(width + 3), row))
            s += '[%s]\n' % rs
        return s


class Vector(Matrix):
    """
    A vector
    """
    def __init__(self, v: list):
        """
        Requires that all elements of v
        are instances of the same type.
        *TYPE RESTRICTED TO NUMBER!
        """
        for e in v:
            assert isinstance(e, Number)
        super().__init__([v, ], usrfmt=False)

    def __len__(self):
        return self.nrows

    def norm(self):
        """
        Returns the 'length' of the vector.
        """
        # Equivalent to sqrt(sum(self.dot(self))):
        return sqrt(sum(map(lambda x: x ** 2, self[0])))

    def rot(self, o, axis=''):
        """
        Returns a rotated view of a vector in space.
        The rotation is counterclockwise by theta,
        about the specified axis when relevant.
        """
        rm = {
            2: {
                '': Matrix([[cos(o), -sin(o)],
                            [sin(o), cos(o)]])
            },
            3: {
                'x': Matrix([[1, 0, 0],
                             [0, cos(o), -sin(o)],
                             [0, sin(o), cos(o)]]),
                'y': Matrix([[cos(o), 0, sin(o)],
                             [0, 1, 0],
                             [-sin(o), 0, cos(o)]]),
                'z': Matrix([[cos(o), -sin(o), 0],
                             [sin(o), cos(o), 0],
                             [0, 0, 1]])
            }
        }  # Rotation matrices based on size
        if len(self) not in rm.keys():
            return
        if o < 0:
            o = ceil(-o / 2 / pi) * 2 * pi + o
        o %= 2 * pi
        return rm[len(self)][axis] * self

    def transform(self):
        """Do not allow transforms on vectors."""
        pass

    def dot(self, other):
        """
        If the vectors are of equal vector length,
        Returns the dot product of this and other.
        """
        if (isinstance(other, Vector) and
                len(self) is len(other)):
            prod = [self[0][i] * other[0][i]
                    for i in range(len(self))]
            return Vector(prod)
        else:
            return NotImplemented

    def __mul__(self, other):
        """Vector cross product"""
        if (isinstance(other, Vector) and
                len(self) is 3 and
                len(self) is len(other)):
            mtx = [[1, -1, 1], self[0], other[0]]
            cross = []  # TODO
            return Vector(cross)
        else:
            return NotImplemented


vec = Vector([0, 1, 2, 3])
mtx = Matrix([[0, 11],   # [0, 11]
              [2,  3]])  # [2,  3]
print(str(5 * vec))
print(str(2 * mtx * mtx))
print((2 * mtx * mtx).det(), 44*62 - 66*12)
