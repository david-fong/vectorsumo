from math import sqrt, pi, ceil, cos, sin, log10
from numbers import Number


class Matrix(list):
    """
    A matrix. A list of equal-length columns.
    """
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
        t = []
        for r in range(self.nrows):
            t.append([self[c][r] for c in range(self.ncols)])
        return Matrix(t, usrfmt=False)

    def det(self):
        pass  # TODO

    def inverse(self):
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

    def norm(self):
        """
        Returns the 'length' of the vector.
        """
        # Equivalent to sqrt(sum(self.dot(self))):
        return sqrt(sum(map(lambda x: x ** 2, self[0])))

    def rot(self, o, axis=''):
        """
        Returns a rotated view of a 2D vector.
        The rotation is counterclockwise by theta.
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
        if self.nrows not in rm.keys():
            return
        if o < 0:
            o = ceil(-o / 2 / pi) * 2 * pi + o
        o %= 2 * pi
        return rm[self.nrows][axis] * self

    def dot(self, other):
        """
        Returns the dot product of this and other
        """
        if (not isinstance(other, Vector) or
                self.nrows is not other.nrows):
            return
        prod = [self[0][i] * other[0][i]
                for i in range(self.nrows)]
        return Vector(prod)


vec = Vector([0, 1, 2, 3])
mtx = Matrix([[0, 11],   # [0, 11]
              [2,  3]])  # [2,  3]
print(str(5 * vec))
print(str(2 * mtx * mtx))
