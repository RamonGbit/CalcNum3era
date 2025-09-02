class SignificantFigures:
    __value = 0

    def __init__(self, value: str):
        self.__value = self.__calculateSignificantFigures(value)

    def __calculateSignificantFigures(self, value: str):
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

    def getValue(self):
        return self.__value

    def __str__(self):
        return str(self.__value)
