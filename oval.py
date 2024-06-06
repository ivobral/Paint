from abstractGraphicalObject import AbstractGraphicalObject
from point import Point
from rectangle import Rectangle
from geometryUtil import GeometryUtil
import math
import numpy as np
from typing import List
from graphicalObject import GraphicalObject
from stack import Stack

class Oval(AbstractGraphicalObject):
    def __init__(self, right_top: Point = Point(100, 0), bottom_left: Point = Point(0, 100)):
        right_top = Point(right_top.x + 1, right_top.y + 1)
        bottom_left = Point(bottom_left.x + 1, bottom_left.y + 1)
        super().__init__([right_top, bottom_left])

    def getShapeID(self):
        return "@OVAL"
    
    def save(self, rows) -> None:
        rows.append(f"{self.getShapeID()} {self.hotPoints[0].x} {self.hotPoints[0].y} {self.hotPoints[1].x} {self.hotPoints[1].y}")

    def load(self, stack: Stack, data: str) -> None:
        parts = data.split()
        right = Point(float(parts[0]), float(parts[1]))
        bottom = Point(float(parts[2]), float(parts[3]))
        stack.push(Oval(right, bottom))

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
        x_min = min(self.hotPoints[0].x, self.hotPoints[1].x)
        y_min = min(self.hotPoints[0].y, self.hotPoints[1].y)
        x_max = max(self.hotPoints[0].x, self.hotPoints[1].x)
        y_max = max(self.hotPoints[0].y, self.hotPoints[1].y)

        return Rectangle(x_min, y_min, x_max - x_min, y_max - y_min)

    def duplicate(self):
        right = self.hotPoints[0]
        bottom = self.hotPoints[1]
        return Oval(right, bottom)
    
    def getShapeName(self):
        return "Oval"
    
    def render(self, renderer):
        # Calculate the center, semi-major axis, and semi-minor axis
        h = (self.hotPoints[0].x + self.hotPoints[1].x) / 2
        k = (self.hotPoints[0].y + self.hotPoints[1].y) / 2
        a = abs(self.hotPoints[0].x - self.hotPoints[1].x) / 2
        b = abs(self.hotPoints[0].y - self.hotPoints[1].y) / 2

        # Generate the angles for the vertices
        angles = np.linspace(0, 2 * np.pi, 300, endpoint=False)

        # Calculate the x and y coordinates of the vertices
        x_points = h + a * np.cos(angles)
        y_points = k + b * np.sin(angles)

        points = []
        for x, y in zip(x_points, y_points):
            points.append(Point(x, y))

        renderer.fillPolygon(points)