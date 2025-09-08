import numpy as np
from Apps.Common.Repositories.CustomNumbers.Number import Number
from Apps.Common.Repositories.FileManager import FileManager

class Binary(Number):
    _digits: np.ndarray = np.array(["0", "1"])
    _base: int = len(_digits)
    path = ".\Apps\Common\Repositories\Errors"
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