import numpy as np
from Apps.Common.Repositories.CustomNumbers.Number import Number

class Binary(Number):
    _digits: np.ndarray = np.array(["0", "1"])
    _base: int = len(_digits)

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
