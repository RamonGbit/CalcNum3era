from __future__ import annotations
import numpy as np
from abc import ABC, abstractmethod
from Apps.Common.Structures.LinkedList import LinkedList
from Apps.Common.Repositories.FileManager import FileManager

class Number(ABC):
    __digits = None
    __base = None
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, value: str):
        try:
            self._validateAndSetValue(value)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"value={value}")
            return None

    def setValue(self, value: str):
        try:
            self._validateAndSetValue(value)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"value={value}")
            return None

    def getValue(self) -> str:
        try:
            return self._value
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"value={getattr(self, '_value', 'undefined')}")
            return None

    def __add__(self, anotherNumber: Number) -> Number:
        try:
            if not isinstance(anotherNumber, self.__class__):
                raise TypeError("Error: No puedes operar números de distinta base")

            maxLength: int = self.__getMaxLength(self._value, anotherNumber.getValue())
            digitsOfNumber1: np.ndarray = self.__getValuesOf(self.getValue(), maxLength)
            digitsOfNumber2: np.ndarray = self.__getValuesOf(
                anotherNumber.getValue(), maxLength
            )
            indexOfCarry: int = 0
            resultDigits: LinkedList = LinkedList()

            for index in range(-1, -maxLength - 1, -1):
                digitOfNumber1: str = digitsOfNumber1[index]
                digitOfNumber2: str = digitsOfNumber2[index]
                indexOfDigit1: int = self.__getIndexOf(digitOfNumber1)
                indexOfDigit2: int = self.__getIndexOf(digitOfNumber2)

                amountOfSteps: int = indexOfDigit1 + indexOfDigit2 + indexOfCarry
                indexOfCarry = 0
                i: int = 0

                for step in range(amountOfSteps):
                    if self.digits[i] == self.digits[-1]:
                        indexOfCarry += 1
                        i = 0
                    else:
                        i += 1

                resultDigits.addFirst(self.digits[i])

            if indexOfCarry > 0:
                resultDigits.addFirst(self.digits[indexOfCarry])

            resultString: str = self.__convertToString(resultDigits)
            resultString = self.__remove_leading_zeros(resultString)
            return self.__class__((resultString))
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, anotherNumber={getattr(anotherNumber, 'getValue', 'undefined')}")
            return None

    def __sub__(self, substrahend: Number) -> Number:
        try:
            if not isinstance(substrahend, self.__class__):
                raise TypeError("Error: No puedes operar números de distinta base")

            maxLength: int = self.__getMaxLength(self.getValue(), substrahend.getValue())
            digitsOfNumber1: np.ndarray = self.__getValuesOf(self.getValue(), maxLength)
            digitsOfNumber2: np.ndarray = self.__getValuesOf(
                substrahend.getValue(), maxLength
            )

            resultDigits: LinkedList = LinkedList()
            additionalLap: int = 0

            for index in range(-1, -maxLength - 1, -1):
                digitOfNumber1: str = digitsOfNumber1[index]
                digitOfNumber2: str = digitsOfNumber2[index]
                indexOfDigit1: int = self.__getIndexOf(digitOfNumber1)
                indexOfDigit2: int = self.__getIndexOf(digitOfNumber2)

                if indexOfDigit1 < indexOfDigit2:
                    for i in range(index - 1, -maxLength - 1, -1):
                        if digitsOfNumber1[i] != "0":
                            borrowSourcePositionInDigits: int = self.__getIndexOf(
                                digitsOfNumber1[i]
                            )
                            digitsOfNumber1[i] = self.digits[
                                borrowSourcePositionInDigits - 1
                            ]
                            additionalLap += 1

                            for j in range(i + 1, index, 1):
                                digitsOfNumber1[j] = self.digits[-1]
                            break

                    remainingSteps: int = indexOfDigit2
                    i: int = -self.base + indexOfDigit1
                    while remainingSteps > 0:
                        while i > -len(self.digits) and remainingSteps > 0:
                            i -= 1
                            remainingSteps -= 1
                        if remainingSteps > 0:
                            additionalLap -= 1
                            remainingSteps -= 1
                            i = -1

                    resultDigits.addFirst(self.digits[i])

                resultString: str = self.__convertToString(resultDigits)
                resultString = self.__remove_leading_zeros(resultString)
                return self.__class__((resultString))
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, substrahend={getattr(substrahend, 'getValue', 'undefined')}")
            return None

    def __mul__(self, multiplier: Number) -> Number:
        try:
            if not isinstance(multiplier, self.__class__):
                raise TypeError("Error: No se pueden operar números de distintas bases")

            if multiplier.getValue() == self.digits[0]:
                return self.__class__(self.digits[0])

            sumsMade: Number = self.__class__(self.digits[1])
            oneSum: Number = self.__class__(self.digits[1])

            result: Number = self.__class__(self.getValue())
            multiplicand: Number = self.__class__(self.getValue())

            while sumsMade != multiplier:
                result += multiplicand
                sumsMade += oneSum

            return result
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, multiplier={getattr(multiplier, 'getValue', 'undefined')}")
            return None

    def __floordiv__(self, anotherNumber: Number) -> Number:
        try:
            if not isinstance(anotherNumber, self.__class__):
                raise TypeError(
                    "Error: No se pueden dividir números de distintos sistemas numéricos"
                )

            if anotherNumber.getValue() == "0":
                raise ZeroDivisionError("Error: División por cero")

            dividend = self.getValue()
            divisor = anotherNumber.getValue()

            if self < anotherNumber:
                return self.__class__("0")

            quotient = ""
            remainder = ""

            for digit in dividend:
                remainder += digit
                remainder = self.__remove_leading_zeros(remainder)

                currentDigit = "0"

                for digit in self.digits[::-1]:
                    if digit == "0":
                        continue

                    product = anotherNumber * self.__class__(digit)
                    if product <= self.__class__(remainder):
                        currentDigit = digit
                        break

                quotient += currentDigit
                product = self.__class__(divisor) * self.__class__(currentDigit)
                remainder = self.__class__(remainder) - product
                remainder = remainder.getValue()

            quotient = self.__remove_leading_zeros(quotient)

            return self.__class__(quotient)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, anotherNumber={getattr(anotherNumber, 'getValue', 'undefined')}")
            return None

    def __lt__(self, anotherNumber: Number) -> bool:
        try:
            if not isinstance(anotherNumber, self.__class__):
                raise TypeError("Error: No puedes comparar numeros de distintas bases")

            a = self.getValue()
            b = anotherNumber.getValue()
            a = self.__remove_leading_zeros(a)
            b = self.__remove_leading_zeros(b)

            if len(self.getValue()) < len(anotherNumber.getValue()):
                return True
            elif len(self.getValue()) > len(anotherNumber.getValue()):
                return False

            for i in range(len(self.getValue())):
                digitOfA = a[i]
                digitOfB = b[i]
                digitOfAPosition = self.__getIndexOf(digitOfA)
                digitOfBPosition = self.__getIndexOf(digitOfB)

                if digitOfAPosition < digitOfBPosition:
                    return True
                elif digitOfAPosition > digitOfBPosition:
                    return False

            return False
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, anotherNumber={getattr(anotherNumber, 'getValue', 'undefined')}")
            return None

    def __le__(self, anotherNumber: Number) -> bool:
        try:
            if not isinstance(anotherNumber, self.__class__):
                raise TypeError("Error: No puedes comparar numeros de distintas bases")

            a = self.getValue()
            b = anotherNumber.getValue()
            a = self.__remove_leading_zeros(a)
            b = self.__remove_leading_zeros(b)

            if len(self.getValue()) < len(anotherNumber.getValue()):
                return True
            elif len(self.getValue()) > len(anotherNumber.getValue()):
                return False

            for i in range(len(self.getValue())):
                digitOfA = a[i]
                digitOfB = b[i]
                digitOfAPosition = self.__getIndexOf(digitOfA)
                digitOfBPosition = self.__getIndexOf(digitOfB)

                if digitOfAPosition < digitOfBPosition:
                    return True
                elif digitOfAPosition > digitOfBPosition:
                    return False

            return True
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, anotherNumber={getattr(anotherNumber, 'getValue', 'undefined')}")
            return None

    def __gt__(self, anotherNumber: Number) -> bool:
        try:
            if not isinstance(anotherNumber, self.__class__):
                raise TypeError("Error: No puedes comparar numeros de distintas bases")

            a = self.getValue()
            b = anotherNumber.getValue()
            a = self.__remove_leading_zeros(a)
            b = self.__remove_leading_zeros(b)

            if len(self.getValue()) > len(anotherNumber.getValue()):
                return True
            elif len(self.getValue()) < len(anotherNumber.getValue()):
                return False

            for i in range(len(self.getValue())):
                digitOfA = a[i]
                digitOfB = b[i]
                digitOfAPosition = self.__getIndexOf(digitOfA)
                digitOfBPosition = self.__getIndexOf(digitOfB)

                if digitOfAPosition > digitOfBPosition:
                    return True
                elif digitOfAPosition < digitOfBPosition:
                    return False

            return False
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, anotherNumber={getattr(anotherNumber, 'getValue', 'undefined')}")
            return None

    def __ge__(self, anotherNumber: Number) -> bool:
        try:
            if not isinstance(anotherNumber, self.__class__):
                raise TypeError("Error: No puedes comparar numeros de distintas bases")

            a = self.getValue()
            b = anotherNumber.getValue()
            a = self.__remove_leading_zeros(a)
            b = self.__remove_leading_zeros(b)

            if len(self.getValue()) > len(anotherNumber.getValue()):
                return True
            elif len(self.getValue()) < len(anotherNumber.getValue()):
                return False

            for i in range(len(self.getValue())):
                digitOfA = a[i]
                digitOfB = b[i]
                digitOfAPosition = self.__getIndexOf(digitOfA)
                digitOfBPosition = self.__getIndexOf(digitOfB)

                if digitOfAPosition > digitOfBPosition:
                    return True
                elif digitOfAPosition < digitOfBPosition:
                    return False
            return True
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, anotherNumber={getattr(anotherNumber, 'getValue', 'undefined')}")
            return None

    def __ne__(self, anotherNumber: Number) -> bool:
        try:
            if not isinstance(anotherNumber, self.__class__):
                raise TypeError("Error: No puedes comparar numeros de distintas bases")

            a = self.getValue()
            b = anotherNumber.getValue()
            a = self.getValue()
            b = anotherNumber.getValue()

            if len(a) != len(b):
                return True

            for i in range(len(a)):
                digitOfA = a[i]
                digitOfB = b[i]
                digitOfAPosition = self.__getIndexOf(digitOfA)
                digitOfBPosition = self.__getIndexOf(digitOfB)

                if digitOfAPosition != digitOfBPosition:
                    return True

            return False
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, anotherNumber={getattr(anotherNumber, 'getValue', 'undefined')}")
            return None

    def __eq__(self, anotherNumber: Number) -> bool:
        try:
            if not isinstance(anotherNumber, self.__class__):
                raise TypeError("Error: No puedes comparar numeros de distintas bases")
            a = self.getValue()
            b = anotherNumber.getValue()

            if len(a) != len(b):
                return False

            for i in range(len(a)):
                digitOfA = a[i]
                digitOfB = b[i]
                digitOfAPosition = self.__getIndexOf(digitOfA)
                digitOfBPosition = self.__getIndexOf(digitOfB)

                if digitOfAPosition != digitOfBPosition:
                    return False

            return True
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_value={getattr(self, '_value', 'undefined')}, anotherNumber={getattr(anotherNumber, 'getValue', 'undefined')}")
            return None

    def __getValuesOf(self, value: str, lenght: int) -> np.ndarray[str]:
        try:
            listOfValues: np.ndarray = np.full(lenght, "0", dtype=object)

            for i in range(-1, -len(value) - 1, -1):
                char: str = value[i]
                listOfValues[i] = char

            return listOfValues
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"value={value}, lenght={lenght}")
            return None

    def __getIndexOf(self, digit: str) -> int:
        try:
            if digit in self._digits:
                for i in range(len(self._digits)):
                    if digit == self._digits[i]:
                        return i
            else:
                raise ValueError(
                    "Error: El valor que has ingresado no pertenece al sistema numérico"
                )
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"digit={digit}")
            return None

    def __getMaxLength(self, digitsOfNumber1: str, digitsOfNumber2: str) -> int:
        try:
            if len(digitsOfNumber1) > len(digitsOfNumber2):
                return len(digitsOfNumber1)
            else:
                return len(digitsOfNumber2)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"digitsOfNumber1={digitsOfNumber1}, digitsOfNumber2={digitsOfNumber2}")
            return None

    def __convertToString(self, valueList: LinkedList) -> str:
        try:
            result: str = ""
            if valueList:
                for i in range(valueList.getSize()):
                    result += valueList.get(i)
                return result
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, "convertToString method")
            return None

    def _validateAndSetValue(self, value: str) -> None:
        try:
            if isinstance(value, str):
                value = value.upper()
                numberOfDecimalPoints: int = 0
                for char in value:
                    if char == "." and numberOfDecimalPoints == 0:
                        numberOfDecimalPoints += 1
                    elif char == "." and numberOfDecimalPoints > 0:
                        raise ValueError(
                            "Error: El valor ingresado posee un formato inválido"
                        )
                    elif char not in self._digits:
                        raise ValueError(
                            "Error: El valor ingresado posee digitos no soportados por el sistema numérico"
                        )
                self._value = value
            else:
                raise ValueError("Error: El valor debe ser expresado en un String")
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"value={value}")
            return None

    def __remove_leading_zeros(self, num: str) -> str:
        try:
            first_non_zero = 0
            digits_list = list(self._digits)
            while first_non_zero < len(num) and num[first_non_zero] == digits_list[0]:
                first_non_zero += 1
            return num[first_non_zero:] if first_non_zero < len(num) else digits_list[0]
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"num={num}")
            return None

    def __str__(self):
        try:
            return f"{self._value} (base {self._base})"
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"value={getattr(self, '_value', 'undefined')}, base={getattr(self, '_base', 'undefined')}")
            return None