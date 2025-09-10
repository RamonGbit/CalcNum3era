from Apps.Common.Repositories.FileManager import FileManager

class SignificantFigures:
    __value = 0
    path = "Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, value: str):
        try:
            self.__value = self.__calculateSignificantFigures(value)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __calculateSignificantFigures(self, value: str):
        try:
            self.__validateInput(value)

            for char in value:
                if char.lower() in "abcdef":
                    return "No aplica"

            significantFigures = 0
            leadingZero = True

            for char in value:
                if char == "0" and significantFigures == 0:
                    continue
                elif char != ".":
                    significantFigures += 1

            return significantFigures
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __validateInput(self, value: str) -> None:
        try:
            if not isinstance(value, str):
                raise ValueError("Error: El valor ingresado debe ser un string")

            validChars = "-.0123456789abcdefABCDEF"

            for char in value:
                if char not in validChars:
                    raise ValueError("Error: El valor ingresado posee caracteres inválidos")

            if value.count(".") > 1:
                raise ValueError(
                    "Error: El formato del número con punto decimal es incorrecto"
                )
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def getValue(self):
        try:
            return self.__value
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __str__(self):
        try:
            return str(self.__value)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None