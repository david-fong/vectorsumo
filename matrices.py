

class Matrix(list):
    """
    A matrix
    """
    nrows: int
    ncols: int

    def __init__(self, m: [[], ]):
        """
        Requires that all elements of grid have equal length.
        """
        self.nrows = len(m)
        self.ncols = len(m[0])
        super().__init__(m)
        for row in self:
            assert len(row) is self.ncols

    def can_add(self, other):
        return (isinstance(other, Matrix) and
                other.nrows is self.nrows and
                other.ncols is self.ncols)

    def __iadd__(self, other):
        # check if matrix addition is valid
        if not self.can_add(other):
            return
        for r in range(self.nrows):
            for c in range(self.ncols):
                self[r][c] += other[r][c]

    def __add__(self, other):
        # check if matrix addition is valid
        if not self.can_add(other):
            return
        sum_grid = []
        for r in range(self.nrows):
            sum_row = []
            for c in range(self.ncols):
                sum_row.append(self[r][c] + other[r][c])
            sum_grid.append(sum_row)
        return sum_grid
