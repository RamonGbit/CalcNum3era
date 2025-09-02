from Apps.Common.Repositories.CustomNumbers.Number import Number
from Apps.Common.Repositories.CustomNumbers.Binary import Binary
from Apps.Common.Repositories.CustomNumbers.Decimal import Decimal
from Apps.Common.Repositories.CustomNumbers.Hexadecimal import Hexadecimal
from Apps.Common.Structures.LinkedList import LinkedList
from Apps.Common.Repositories.StudiedNumbers.Components.NumeralSystem import NumeralSystem


class ElementaryOperations:
    availableNumeralSystems: dict[str:Number] = {
        "binario": Binary,
        "decimal": Decimal,
        "hexadecimal": Hexadecimal,
    }

    __validOperationCache: dict[str:LinkedList] = None

    def __init__(self, numeralSystems: NumeralSystem):
        if not isinstance(numeralSystems, NumeralSystem):
            raise ValueError("Error: Has ingresado sistemas numéricos inválidos")

        if ElementaryOperations.__validOperationCache is None:
            ElementaryOperations.__validOperationCache = {}
            ElementaryOperations._initializeOperationCache()

        self.__operations: LinkedList = LinkedList()
        self.__checkElementaryOperations(numeralSystems)

    @classmethod
    def _initializeOperationCache(cls):
        for numeralSystemName in cls.availableNumeralSystems.keys():
            numeralSystem: Number = cls.availableNumeralSystems.get(numeralSystemName)
            elementaryOperations: LinkedList = cls.__checkElementaryOperationsOf(
                numeralSystem
            )
            cls.__validOperationCache[numeralSystemName] = elementaryOperations

    @classmethod
    def __checkElementaryOperationsOf(cls, numeralSystem: Number) -> LinkedList:
        if not issubclass(numeralSystem, Number):
            raise ValueError("Error: Haz ingresado un sistema numérico inválido")

        elementaryOperations = LinkedList()
        operationsToTest = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "//": lambda a, b: a // b,
        }

        testDigit: str = numeralSystem.getDigits()[1]
        numberToTest: Number = numeralSystem(testDigit)

        for operation in operationsToTest.keys():
            try:
                operationsToTest.get(operation)(numberToTest, numberToTest)
                elementaryOperations.addLast(operation)
            except (TypeError, NotImplementedError) as error:
                pass

        return elementaryOperations

    def __checkElementaryOperations(self, numeralSystems: NumeralSystem):
        lists = LinkedList()
        numeralSystems = numeralSystems.getSystem()

        for i in range(numeralSystems.getSize()):
            availableOperations: LinkedList = (
                ElementaryOperations.__validOperationCache.get(numeralSystems.get(i))
            )
            lists.addLast(availableOperations)

        elementaryOperations = self.__findMinorList(lists)
        self.__operations = elementaryOperations

    def __findMinorList(self, lists: LinkedList) -> LinkedList:
        if not lists:
            raise ValueError("Error: La lista de listas es inválida")

        systemWithLessOperationsIndex: int = 0
        for i in range(lists.getSize()):
            if (
                lists.get(i).getSize()
                < lists.get(systemWithLessOperationsIndex).getSize()
            ):
                systemWithLessOperationsIndex = i

        return lists.get(systemWithLessOperationsIndex)

    def __str__(self):
        text = ""
        for i in range(self.__operations.getSize()):
            if i == self.__operations.getSize() - 1:
                text += f"{self.__operations.get(i)}"
            else:
                text += f"{self.__operations.get(i)}, "
        return text

    def __validateValue(self, value: str) -> None:
        if value.__class__.__name__ == "str":
            validChars = "-.0123456789abcdefABCDEF"

            numberOfPoints = 0
            for char in value:
                if char not in validChars:
                    raise ValueError(
                        "Error: El valor ingresado posee caracteres no válidos"
                    )
                elif char == "." and numberOfPoints == 1:
                    raise ValueError(
                        "Error: El formato del número con punto decimal es incorrecto"
                    )
                elif char == ".":
                    numberOfPoints += 1
        else:
            raise ValueError("Error: El valor ingresado debe ser un string")
