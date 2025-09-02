from .Node import Node


class LinkedList:
    def __init__(self):
        self.__head: Node = None
        self.__tail: Node = None
        self.__size = 0

    def isEmpty(self) -> bool:
        return self.__size == 0

    def getSize(self) -> int:
        return self.__size

    def get(self, index: int) -> any:
        if index < -self.__size or index >= self.__size:
            raise IndexError("Error: El índice es inválido")
        if index >= 0:
            current = self.__head
            for i in range(index):
                current = current.getNext()
            return current.getData()
        else:
            current = self.__tail
            i = -1
            while i != index:
                current = current.getPrev()
                i -= 1
            return current.getData()

    def addLast(self, data: any) -> None:
        newNode: Node = Node(data)

        if self.isEmpty():
            self.__head = newNode
            self.__tail = newNode
        else:
            newNode.setPrev(self.__tail)
            self.__tail.setNext(newNode)
            self.__tail = newNode
        self.__size += 1

    def addFirst(self, data: any) -> None:
        nuevo_nodo = Node(data)

        if self.isEmpty():
            self.__head = nuevo_nodo
            self.__tail = nuevo_nodo
        else:
            nuevo_nodo.setNext(self.__head)
            self.__head.setPrev(nuevo_nodo)
            self.__head = nuevo_nodo

        self.__size += 1

    def removeLast(self) -> None:
        if self.isEmpty():
            raise IndexError("Error: La lista está vacía")

        data = self.__tail.getData()

        if self.__size == 1:
            self.__head = None
            self.__tail = None
        else:
            self.__tail = self.__tail.getPrev()
            self.__tail.setNext(None)

        self.__size -= 1
        return data

    def contains(self, data: any) -> bool:
        current = self.__head
        while current is not None:
            if current.getData() == data:
                return True
            current = current.getNext()
        return False

    def printList(self) -> None:
        actual = self.__head
        while actual:
            print(actual.getData(), end=" <-> ")
            actual = actual.getNext()
        print()
