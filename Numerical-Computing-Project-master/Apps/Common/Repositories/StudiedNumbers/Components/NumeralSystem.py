from Apps.Common.Structures.LinkedList import LinkedList


class NumeralSystem:

    def __init__(self, value: str):
        self.__systems: LinkedList = LinkedList()
        self.__validateInput(value)
        self.__determineNumeralSystems(value)

    def __determineNumeralSystems(self, value: str):
        if self.__isBinary(value):
            self.__systems.addLast("binario")

        if self.__isDecimal(value):
            self.__systems.addLast("decimal")

        if self.__isHexadecimal(value):
            self.__systems.addLast("hexadecimal")

    def __isBinary(self, value: str) -> bool:
        validChars = "-.01"
        for char in value:
            if char not in validChars:
                return False
        return True

    def __isDecimal(self, value: str) -> bool:
        validChars = "-.0123456789"

        for char in value:
            if char not in validChars:
                return False
        return True

    def __isHexadecimal(self, value: str) -> bool:
        validChars = "-.0123456789abcdefABCDEF"

        for char in value:
            if char not in validChars:
                return False
        return True

    def getSystem(self):
        return self.__systems

    def __str__(self):
        text = ""
        for i in range(self.__systems.getSize()):
            if i == self.__systems.getSize() - 1:
                text += f"{self.__systems.get(i)}"
            else:
                text += f"{self.__systems.get(i)}, "
        return text

    def __validateInput(self, value: str) -> None:
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
