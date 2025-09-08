from Apps.Common.Structures.LinkedList import LinkedList
from Apps.Common.Repositories.FileManager import FileManager

class NumeralSystem:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, value: str):
        try:
            self.__systems: LinkedList = LinkedList()
            self.__validateInput(value)
            self.__determineNumeralSystems(value)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __determineNumeralSystems(self, value: str):
        try:
            if self.__isBinary(value):
                self.__systems.addLast("binario")

            if self.__isDecimal(value):
                self.__systems.addLast("decimal")

            if self.__isHexadecimal(value):
                self.__systems.addLast("hexadecimal")
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __isBinary(self, value: str) -> bool:
        try:
            validChars = "-.01"
            for char in value:
                if char not in validChars:
                    return False
            return True
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __isDecimal(self, value: str) -> bool:
        try:
            validChars = "-.0123456789"

            for char in value:
                if char not in validChars:
                    return False
            return True
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __isHexadecimal(self, value: str) -> bool:
        try:
            validChars = "-.0123456789abcdefABCDEF"

            for char in value:
                if char not in validChars:
                    return False
            return True
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def getSystem(self):
        try:
            return self.__systems
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __str__(self):
        try:
            text = ""
            for i in range(self.__systems.getSize()):
                if i == self.__systems.getSize() - 1:
                    text += f"{self.__systems.get(i)}"
                else:
                    text += f"{self.__systems.get(i)}, "
            return text
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