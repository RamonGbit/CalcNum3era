import numpy as np
from errors import createLogFile
from Apps.Common.Repositories.FileManager import FileManager

class Conversor:

    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    @staticmethod
    def convertToDecimal(number: str, base: int) -> float:
        try:
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
        except Exception as error:
            createLogFile(Conversor, error, error.__traceback__, number)
            return None

    @staticmethod
    def convertEveryValueToFloat(matrix: np.ndarray) -> np.ndarray:
        try:
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    try:
                        if Conversor.isHexadecimal(matrix[i][j]):
                            if matrix[i][j]:
                                matrix[i][j] = Conversor.convertToDecimal(matrix[i][j], 16)
                            else:
                                matrix[i][j] = 0
                        if matrix[i][j]:
                            matrix[i][j] = float(matrix[i][j])
                        else:
                            matrix[i][j] = 0.0
                    except ValueError:
                        # Ignorar errores de conversión individuales
                        continue
            return matrix
        except Exception as error:
            createLogFile(Conversor, error, error.__traceback__, "convertEveryValueToFloat")
            return None

    @staticmethod
    def isHexadecimal(value: str) -> bool:
        try:
            if value:
                letters = "abcdefABCDEF"
                for char in value:
                    if char in letters:
                        return True
                return False
            return False
        except Exception as error:
            createLogFile(Conversor, error, error.__traceback__, "isHexadecimal")
            return False
