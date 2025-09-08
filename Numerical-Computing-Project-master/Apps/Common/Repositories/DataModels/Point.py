import math
from Apps.Common.Repositories.FileManager import FileManager

class Point:
    path = ".\Apps\Common\Repositories\Errors"
    fileManager = FileManager(path)

    def __init__(self, name, position):
        try:
            self.name = name
            self.position = position
            self.pointGroup = None
            self.distancesBetweenPoints = None
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"name={name}, position={position}")
            return None
    
    def getName(self):
        try:
            return self.name
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"name={getattr(self, 'name', 'undefined')}")
            return None
    
    def getPosition(self):
        try:
            return self.position
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"position={getattr(self, 'position', 'undefined')}")
            return None

    def setPointGroup(self, pointGroup):
        try:
            self.pointGroup = pointGroup
            self.distancesBetweenPoints = {}

            for otherPoint in pointGroup:
                if otherPoint != self:
                    distance = self.calculateDistance(otherPoint)
                    self.distancesBetweenPoints[otherPoint.name] = distance
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"pointGroup={pointGroup}")
            return None
    
    def calculateDistance(self, otherPoint):
        try:
            x1, y1, z1 = self.position
            x2, y2, z2 = otherPoint.position
            return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"self_position={getattr(self, 'position', 'undefined')}, otherPoint_position={getattr(otherPoint, 'position', 'undefined')}")
            return None

    def toDict(self):
        try:
            return {
                'name': self.name,
                'position': list(self.position),
                'distancesBetweenPoints': self.distancesBetweenPoints
            }
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"name={getattr(self, 'name', 'undefined')}, position={getattr(self, 'position', 'undefined')}, distancesBetweenPoints={getattr(self, 'distancesBetweenPoints', 'undefined')}")
            return None
    
    def __repr__(self):
        try:
            return f"Point(name='{self.name}', position={self.position})"
        except Exception as error:
            from errors import createLogFile
            createLogFile(self.fileManager   , error, error.__traceback__, f"name={getattr(self, 'name', 'undefined')}, position={getattr(self, 'position', 'undefined')}")
            return None