import numpy as np
from Apps.Common.Repositories.CustomNumbers.Number import Number

class Hexadecimal(Number):
    _digits = np.array(
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    )
    _base = len(_digits)

    def __init__(self, value: str):
        super().__init__(value)

    def value(self):
        return self._value

    @property
    def digits(self):
        return self._digits

    @classmethod
    def getDigits(self):
        return self._digits

    def base(self):
        return self._base
