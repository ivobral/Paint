from typing import List
from abstractGraphicalObject import AbstractGraphicalObject
from graphicalObject import GraphicalObject
from point import Point
from geometryUtil import GeometryUtil
from rectangle import Rectangle
from stack import Stack

class LineSegment(AbstractGraphicalObject):
    def __init__(self, start: Point = Point(0, 0), end: Point = Point(100, 20)):
        start = Point(start.x + 1, start.y + 1)
        end = Point(end.x + 1, end.y + 1)
        super().__init__([start, end])

    def getShapeID(self):
        return "@LINE"
    
    def save(self, rows) -> None:
        rows.append(f"{self.getShapeID()} {self.hotPoints[0].x} {self.hotPoints[0].y} {self.hotPoints[1].x} {self.hotPoints[1].y}")

    def load(self, stack: Stack, data: str) -> None:
        parts = data.split()
        start = Point(float(parts[0]), float(parts[1]))
        end = Point(float(parts[2]), float(parts[3]))
        stack.push(LineSegment(start, end))

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

    def render(self, renderer):
        renderer.drawLine(self.hotPoints[0], self.hotPoints[1])