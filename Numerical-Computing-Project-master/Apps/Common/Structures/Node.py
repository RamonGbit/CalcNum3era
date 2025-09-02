from __future__ import annotations


class Node:
    def __init__(self, data: any = None):
        self.__data: any = data
        self.__next = None
        self.__prev = None

    def getData(self) -> any:
        return self.__data

    def getNext(self) -> Node:
        return self.__next

    def getPrev(self) -> Node:
        return self.__prev

    def setData(self, data):
        self.__data = data

    def setNext(self, nextNode: Node):
        self.__next = nextNode

    def setPrev(self, prevNode: Node):
        self.__prev = prevNode
