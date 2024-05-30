from abstractGraphicalObject import AbstractGraphicalObject
from point import Point
from rectangle import Rectangle
from geometryUtil import GeometryUtil
import math

class Oval(AbstractGraphicalObject):
    def __init__(self, right_top: Point = Point(10, 0), bottom_left: Point = Point(0, 10)):
        super().__init__([right_top, bottom_left])

    def selectionDistance(self, mousePoint: Point):
        # Središte elipse kao točka na sredini između dvije točke
        center = Point(self.hotPoints[0].x, self.hotPoints[1].y)
        # Radijusi elipse kao udaljenosti od središta do točaka na rubu
        radiusX = GeometryUtil.distanceFromPoint(center, self.hotPoints[0])
        radiusY = GeometryUtil.distanceFromPoint(center, self.hotPoints[1])

    	# Ako je točka unutar elipse, udaljenost je 0
        if (mousePoint.x - center.x) ** 2 / radiusX ** 2 + (mousePoint.y - center.y) ** 2 / radiusY ** 2 <= 1:
            return 0
        
        min_distance = -1
        n_points = 100

        # Pronađi najmanju udaljenost od točke do elipse
        for i in range(n_points):
            p = Point(center.x + radiusX * math.cos(2 * math.pi * i / n_points),
                        center.y + radiusY * math.sin(2 * math.pi * i / n_points))
            
            distance = GeometryUtil.distanceFromPoint(p, mousePoint)
            if min_distance == -1 or distance < min_distance:
                min_distance = distance
        
        return min_distance

    def getBoundingBox(self):
        left_bottom = Point(self.hotPoints[0].x - (self.hotPoints[1].x - self.hotPoints[0].x),
                            self.hotPoints[0].y)
        right_top = Point(self.hotPoints[1].x,
                          self.hotPoints[1].y + (self.hotPoints[1].y - self.hotPoints[0].y))
        
        minX = min(left_bottom.x, right_top.x)
        minY = min(left_bottom.y, right_top.y)
        maxX = max(left_bottom.x, right_top.x)
        maxY = max(left_bottom.y, right_top.y)

        return Rectangle(minX, minY, maxX - minX, maxY - minY)

    def duplicate(self):
        right = self.hotPoints[0]
        bottom = self.hotPoints[1]
        return Oval(right, bottom)
    
    def getShapeName(self):
        return "Oval"