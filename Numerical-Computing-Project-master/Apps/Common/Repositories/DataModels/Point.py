import math

class Point:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.pointGroup = None
        self.distancesBetweenPoints = None
    
    def getName(self):
        return self.name
    
    def getPosition(self):
        return self.position

    def setPointGroup(self, pointGroup):
        self.pointGroup = pointGroup
        self.distancesBetweenPoints = {}

        for otherPoint in pointGroup:
            if otherPoint != self:
                distance = self.calculateDistance(otherPoint)
                self.distancesBetweenPoints[otherPoint.name] = distance
    
    def calculateDistance(self, otherPoint):
        x1, y1, z1 = self.position
        x2, y2, z2 = otherPoint.position
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

    def toDict(self):
        return {
            'name': self.name,
            'position': list(self.position),
            'distancesBetweenPoints': self.distancesBetweenPoints
        }
    
    def __repr__(self):
        return f"Point(name='{self.name}', position={self.position})"