from Apps.Common.Structures.LinkedList import LinkedList
from Apps.Common.Repositories.StudiedNumbers.Components.NumeralSystem import NumeralSystem

class Bases:
    def __init__(self, numeralSystem: NumeralSystem):
        self.__bases = LinkedList()
        self.__checkAndSetBases(numeralSystem.getSystem())

    def __checkAndSetBases(self, numeralSystems: LinkedList):
        bases: dict[str:str] = {
            "binario": "base 2",
            "decimal": "base 10",
            "hexadecimal": "base 16",
        }
        for i in range(numeralSystems.getSize()):
            self.__bases.addLast(bases[numeralSystems.get(i)])

    def __str__(self) -> str:
        text = ""
        for i in range(self.__bases.getSize()):
            if i == self.__bases.getSize() - 1:
                text += f"{self.__bases.get(i)}"
            else:
                text += f"{self.__bases.get(i)}, "
        return text
