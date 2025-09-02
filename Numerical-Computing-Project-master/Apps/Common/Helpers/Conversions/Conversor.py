import numpy as np


class Conversor:
    @staticmethod
    def convertToDecimal(number: str, base: int) -> float:
        digits = "0123456789ABCDEF"
        number = number.upper()

        if "." in number:
            integerPart, fractionPart = number.split(".")
        else:
            integerPart, fractionPart = number, ""

        decimal = 0
        for i, char in enumerate(integerPart[::-1]):
            if char not in digits[:base]:
                raise ValueError(f"Dígito inválido: {char} para base {base}")
            decimal += digits.index(char) * (base**i)

        for i, char in enumerate(fractionPart, start=1):
            if char not in digits[:base]:
                raise ValueError(f"Dígito inválido: {char} para base {base}")
            decimal += digits.index(char) * (base**-i)

        if number[0] == "-":
            return -decimal

        return decimal

    @staticmethod
    def convertEveryValueToFloat(matrix: np.ndarray) -> np.ndarray:

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if Conversor.isHexadecimal(matrix[i][j]):
                    try:
                        if matrix[i][j]:
                            matrix[i][j] = Conversor.convertToDecimal(matrix[i][j], 16)
                        else:
                            matrix[i][j] = 0
                    except ValueError as error:
                        continue
                if matrix[i][j]:
                    matrix[i][j] = float(matrix[i][j])
                else:
                    matrix[i][j] = 0.0
        return matrix

    @staticmethod
    def isHexadecimal(value: str) -> bool:
        if value:
            letters = "abcdefABCDEF"
            for char in value:
                if char in letters:
                    return True
            return False
