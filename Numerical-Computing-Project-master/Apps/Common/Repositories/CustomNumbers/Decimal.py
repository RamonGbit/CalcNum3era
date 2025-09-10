from __future__ import annotations
import numpy as np
from Apps.Common.Repositories.CustomNumbers.Number import Number
from Apps.Common.Repositories.FileManager import FileManager

class Decimal(Number):
    _digits = np.array(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
    _base = len(_digits)
    path = "Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, value: str):
        try:
            super().__init__(value)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"value={value}")
            return None

    def value(self):
        try:
            return self._value
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"value={getattr(self, '_value', 'undefined')}")
            return None

    @property
    def digits(self):
        try:
            return self._digits
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, "digits property")
            return None

    @classmethod
    def getDigits(self):
        try:
            return self._digits
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, "getDigits classmethod")
            return None

    def base(self):
        try:
            return self._base
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, "base method")
            return None

    def __truediv__(self, anotherValue: Decimal):
        try:
            return Decimal(str(int(self._value) // int(anotherValue.value())))
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, anotherValue={getattr(anotherValue, 'value', 'undefined')}")
            return None