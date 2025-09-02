from Apps.Common.Structures.Node import Node

class Queue:
    def __init__(self):
        self.front = None
        self.last = None
        self.size = 0
    
    def enqueue(self, data):
        if data is None:
            raise ValueError("- QueueError: El dato es nulo, no pudo ser agregado a la cola")
        
        newNode = Node(data=data)
        
        if self.isEmpty():
            self.front = newNode
        else:
            self.last.setNext(newNode)
        self.last = newNode
        
        self.size += 1
    
    def dequeue(self):
        if self.isEmpty():
            raise ValueError("- QueueError: la cola esta vacia")
        
        data = self.front.getData()
        self.front = self.front.getNext()
        
        if self.front is None:
            self.last = None
        
        self.size -= 1
        return data
    
    def getPeek(self):
        if self.isEmpty():
            raise ValueError("- QueueError: la cola esta vacia")
        return self.front.getData()
    
    def getSize(self):
        return self.size
    
    def showLast(self):
        print(self.last)
    
    def isEmpty(self):
        return self.front is None and self.size == 0 # type: ignore