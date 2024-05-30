from abstractGraphicalObject import AbstractGraphicalObject
from point import Point
from geometryUtil import GeometryUtil
from rectangle import Rectangle

class LineSegment(AbstractGraphicalObject):
    def __init__(self, start: Point = Point(0, 0), end: Point = Point(10, 0)):
        super().__init__([start, end])

    def selectionDistance(self, mousePoint: Point):
        return GeometryUtil.distanceFromLineSegment(self.hotPoints[0], self.hotPoints[1], mousePoint)
    
    def getBoundingBox(self):
        minX = min(self.hotPoints[0].x, self.hotPoints[1].x)
        minY = min(self.hotPoints[0].y, self.hotPoints[1].y)
        maxX = max(self.hotPoints[0].x, self.hotPoints[1].x)
        maxY = max(self.hotPoints[0].y, self.hotPoints[1].y)
        return Rectangle(minX, minY, maxX - minX, maxY - minY)

    def duplicate(self):
        start = self.hotPoints[0]
        end = self.hotPoints[1]
        return LineSegment(start, end)
    
    def getShapeName(self):
        return "Linija"