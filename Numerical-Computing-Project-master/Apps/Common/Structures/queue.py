from Apps.Common.Structures.Node import Node
from Apps.Common.Repositories.FileManager import FileManager

class Queue:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self):
        try:
            self.front = None
            self.last = None
            self.size = 0
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None
    
    def enqueue(self, data):
        try:
            if data is None:
                raise ValueError("- QueueError: El dato es nulo, no pudo ser agregado a la cola")
            
            newNode = Node(data=data)
            
            if self.isEmpty():
                self.front = newNode
            else:
                self.last.setNext(newNode)
            self.last = newNode
            
            self.size += 1
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None
    
    def dequeue(self):
        try:
            if self.isEmpty():
                raise ValueError("- QueueError: la cola esta vacia")
            
            data = self.front.getData()
            self.front = self.front.getNext()
            
            if self.front is None:
                self.last = None
            
            self.size -= 1
            return data
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None
    
    def getPeek(self):
        try:
            if self.isEmpty():
                raise ValueError("- QueueError: la cola esta vacia")
            return self.front.getData()
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
    
    def showLast(self):
        try:
            print(self.last)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None
    
    def isEmpty(self):
        try:
            return self.front is None and self.size == 0 # type: ignore
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, line)
            return None