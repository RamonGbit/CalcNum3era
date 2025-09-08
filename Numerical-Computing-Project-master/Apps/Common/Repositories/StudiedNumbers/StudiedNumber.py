from Apps.Common.Helpers.ErrorHandling.Exceptions import *
from Apps.Common.Repositories.StudiedNumbers.Components.SignificantFigures import SignificantFigures
from Apps.Common.Repositories.StudiedNumbers.Components.NumeralSystem import NumeralSystem
from Apps.Common.Repositories.StudiedNumbers.Components.Bases import Bases
from Apps.Common.Repositories.StudiedNumbers.Components.ElementaryOperations import ElementaryOperations
from Apps.Common.Repositories.FileManager import FileManager

class StudiedNumber:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, value: str):
        try:
            self.__validateAndSetValue(value)
            self.__significantFigures: SignificantFigures = SignificantFigures(value)
            self.__numeralSystem: NumeralSystem = NumeralSystem(value)
            self.__bases: Bases = Bases(self.__numeralSystem)
            self.__elementaryOperations: ElementaryOperations = ElementaryOperations(
                self.__numeralSystem
            )
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __validateAndSetValue(self, value: str) -> None:
        try:
            if value is None:
                raise NoneType("Error: Has ingresado un valor nulo")
            if not isinstance(value, str):
                raise ValueError("Error: El valor ingresado debe ser un string")

            validChars = "-.0123456789abcdefABCDEF"

            for char in value:
                if char not in validChars:
                    raise NumberIsInvalid(
                        "Error: El valor ingresado posee caracteres inválidos"
                    )

                if value.count(".") > 1:
                    raise NumberIsInvalid(
                        "Error: El formato del número con punto decimal es incorrecto"
                    )

                self.__value = value
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __str__(self) -> str:
        try:
            return f"""
Valor: {self.__value}
Cifras significativas: {self.__significantFigures}
Sistemas numéricos posibles: {self.__numeralSystem}
Bases posibles: {self.__bases}
Operaciones elementales que se pueden realizar en este sistema: {self.__elementaryOperations}
        """
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None