from math import sqrt, pi, ceil, cos, sin
from numbers import Number


class Matrix(list):
    """
    A matrix
    """
    nrows: int
    ncols: int

    def __init__(self, m: [[], ]):
        """
        Requires that all elements of m
        are lists of equal length.
        """
        self.nrows = len(m)
        self.ncols = len(m[0])
        super().__init__(m)

    def __can_add(self, other):
        return (other.nrows is self.nrows and
                other.ncols is self.ncols)

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
        for r in range(self.nrows):
            for c in range(self.ncols):
                self[r][c] += other[r][c]

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
        sum_grid = []
        for r in range(self.nrows):
            sum_row = []
            for c in range(self.ncols):
                sum_row.append(self[r][c] + other[r][c])
            sum_grid.append(sum_row)
        return sum_grid

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.ncols is not other.nrows:
                return
            prod = []
            for r in range(self.nrows):
                row = []
                for c in range(other.ncols):
                    entry = 0
                    for i in range(self.ncols):
                        entry += self[r][i] * other[i][c]
                    row.append(entry)
                prod.append(row)
            return Matrix(prod)
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Number):
            m = []
            for r in range(self.nrows):
                m.append([e * other for e in self[r]])
            return m
        else:
            return NotImplemented


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
            assert isinstance(e, (int, float))
        super().__init__(v)

    def norm(self):
        """
        Returns the 'length' of the vector.
        """
        return sqrt(sum(map(lambda x: x ** 2, self)))

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
            o = (ceil(-o / (2 * pi)) *
                 2 * pi + o) % (2 * pi)
        o %= 2 * pi
        return rm[self.nrows][axis] * self
