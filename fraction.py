from numbers import Number

TEN = (2, 5)


class Fraction(Number):
    numer: list = []
    denom: list = []
    neg: bool

    def __init__(self, numer=0, denom=1):


    @staticmethod
    def factorize(num:int):

        if isinstance(num, float):
            # TODO; return
