from Apps.Common.Structures.Node import Node
from Apps.Common.Repositories.FileManager import FileManager

class Stack:
    path = "Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self):
        try:
            self.stack = None
            self.size = 0
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None
    
    def push(self, data):
        try:
            new_node = Node(data=data)
            new_node.setNext(self.stack)
            self.stack = new_node
            self.size += 1
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None
    
    def pop(self):
        try:
            if self.isEmpty():
                raise ValueError("- StackError: la pila esta vacia")
            data = self.stack.getData()
            self.stack = self.stack.getNext()
            self.size -= 1
            return data
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None
    
    def showStack(self):
        try:
            if self.isEmpty():
                raise ValueError("- StackError: la pila esta vacia")
            return self.stack.getData()
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None
    
    def getSize(self):
        try:
            return self.size
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None
    
    def isEmpty(self):
        try:
            return self.stack is None and self.size == 0
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None