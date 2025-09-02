from Apps.Common.Structures.Node import Node

class Stack:
    def __init__(self):
        self.stack = None
        self.size = 0
    
    def push(self, data):
        new_node = Node(data=data)
        new_node.setNext(self.stack)
        self.stack = new_node
        self.size += 1
    
    def pop(self):
        if self.isEmpty():
            raise ValueError("- StackError: la pila esta vacia")
        data = self.stack.getData()
        self.stack = self.stack.getNext()
        self.size -= 1
        return data
    
    def showStack(self):
        if self.isEmpty():
            raise ValueError("- StackError: la pila esta vacia")
        return self.stack.getData()
    
    def getSize(self):
        return self.size
    
    def isEmpty(self):
        return self.stack is None and self.size == 0