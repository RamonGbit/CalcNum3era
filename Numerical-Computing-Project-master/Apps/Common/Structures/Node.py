from __future__ import annotations
from Apps.Common.Repositories.FileManager import FileManager

class Node:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, data: any = None):
        try:
            self.__data: any = data
            self.__next = None
            self.__prev = None
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def getData(self) -> any:
        try:
            return self.__data
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def getNext(self) -> Node:
        try:
            return self.__next
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def getPrev(self) -> Node:
        try:
            return self.__prev
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def setData(self, data):
        try:
            self.__data = data
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def setNext(self, nextNode: Node):
        try:
            self.__next = nextNode
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None

    def setPrev(self, prevNode: Node):
        try:
            self.__prev = prevNode
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None