from Apps.Common.Structures.LinkedList import LinkedList
from Apps.Common.Repositories.StudiedNumbers.Components.NumeralSystem import NumeralSystem
from Apps.Common.Repositories.FileManager import FileManager

class Bases:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, numeralSystem: NumeralSystem):
        try:
            self.__bases = LinkedList()
            self.__checkAndSetBases(numeralSystem.getSystem())
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __checkAndSetBases(self, numeralSystems: LinkedList):
        try:
            bases: dict[str:str] = {
                "binario": "base 2",
                "decimal": "base 10",
                "hexadecimal": "base 16",
            }
            for i in range(numeralSystems.getSize()):
                self.__bases.addLast(bases[numeralSystems.get(i)])
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def __str__(self) -> str:
        try:
            text = ""
            for i in range(self.__bases.getSize()):
                if i == self.__bases.getSize() - 1:
                    text += f"{self.__bases.get(i)}"
                else:
                    text += f"{self.__bases.get(i)}, "
            return text
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None