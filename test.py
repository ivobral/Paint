from abstractGraphicalObject import AbstractGraphicalObject
from documentModel import DocumentModel
from geometryUtil import GeometryUtil
from graphicalObject import GraphicalObject
from graphicalObjectListener import GraphicalObjectListener
from lineSegment import LineSegment
from oval import Oval
from point import Point
from rectangle import Rectangle
from renderer import Renderer
from GUI import GUI
from tkinter import *

# working before 1 +
root = Tk()
GUI(root, width=400, height=400, bg="white")
root.mainloop()

# working before 2 +
# GraphicalObject je dobar
# Rectangle je dobar
r = Rectangle(0, 0, 10, 10)
print("Rectangle r is:", r.getX(), r.getY(), r.getWidth(), r.getHeight())  # 0 0 10 10
# Point je dobar
p = Point(0, 0)
print("Point p is:", p.getX(), p.getY())  # 0 0
newp = p.translate(Point(10, 5))
print("Point p is after translation:", newp.getX(), newp.getY())  # 10 5
newwp = p.difference(newp)
print("Difference between point p and newp is:", newwp.getX(), newwp.getY())  # -10 -5
# GeometryUtil.distanceFromPoint je dobar
s = Point(0, 0)
e = Point(10, 0)
print("Distance from point (0, 0) to point (10, 0) is:", GeometryUtil.distanceFromPoint(s, e))  # 10.0
s = Point(0, 0)
e = Point(10, 5)
print("Distance from point (0, 0) to point (10, 5) is:", GeometryUtil.distanceFromPoint(s, e))  # 11.180339887498949
# GeometryUtil.distanceFromLineSegment je dobar
s = Point(0, 0)
e = Point(10, 0)
p = Point(5, 5)
print("Distance from point (5, 5) to line segment (0, 0) - (10, 0) is:", GeometryUtil.distanceFromLineSegment(s, e, p))  # 5.0
s = Point(0, 0)
e = Point(10, 5)
p = Point(5, 5)
print("Distance from point (5, 5) to line segment (0, 0) - (10, 5) is:", GeometryUtil.distanceFromLineSegment(s, e, p))  # 2.23606797749979
s = Point(2, 2)
e = Point(2, 2)
p = Point(2, 8)
print("Distance from point (2, 8) to line segment (2, 2) - (2, 2) is:", GeometryUtil.distanceFromLineSegment(s, e, p))  # 6.0
s = Point(2, 2)
e = Point(8, 2)
p = Point(0, 10)
print("Distance from point (0, 10) to line segment (2, 2) - (8, 2) is:", GeometryUtil.distanceFromLineSegment(s, e, p))  # 8.246211251235321
s = Point(2, 4)
e = Point(8, 2)
p = Point(0, 10)
print("Distance from point (0, 10) to line segment (2, 4) - (8, 2) is:", GeometryUtil.distanceFromLineSegment(s, e, p))  # 6.324555320336759
s = Point(2, 4)
e = Point(8, 2)
p = Point(10, 0)
print("Distance from point (10, 0) to line segment (2, 4) - (8, 2) is:", GeometryUtil.distanceFromLineSegment(s, e, p))  # 2.8284271247461903
# GraphicalObjectListener je dobar
# Renderer je dobar
# abstractGraphicalObject
# Create some points
points = [Point(0, 0), Point(1, 1), Point(2, 2)]

# Create an AbstractGraphicalObject
obj = AbstractGraphicalObject(points)

# Test setSelected and isSelected +
#obj.setSelected(True)
#assert obj.isSelected() == True
#obj.setSelected(False)
#assert obj.isSelected() == False

# Test getNumberOfHotPoints
assert obj.getNumberOfHotPoints() == 3

# Test getHotPoint
assert obj.getHotPoint(0) == points[0]

"""
 # Test setHotPoint
obj.setHotPoint(0, Point(5, 5))
assert obj.getHotPoint(0) == points[0]

# Test setHotPointSelected
obj.setHotPointSelected(1, True)
assert obj.isHotPointSelected(1) == True


# Test getHotPointDistance
distance = obj.getHotPointDistance(2, Point(3, 3))
assert distance == ((2 - 3) ** 2 + (2 - 3) ** 2) ** 0.5

# Test translate
obj.translate(Point(2, 2))
p = obj.getHotPoint(0)

assert p.x == 2
assert p.y == 2
"""
#sve radi do sada

ls = LineSegment(Point(0, 0), Point(2, 2))
print(ls.getShapeName())

print(ls.getBoundingBox().getX())
print(ls.getBoundingBox().getY())
print(ls.getBoundingBox().getWidth())
print(ls.getBoundingBox().getHeight())

print(ls.getHotPoint(0).getX())
print(ls.getHotPoint(0).getY())
print(ls.getHotPoint(1).getX())
print(ls.getHotPoint(1).getY())

print(ls.selectionDistance(Point(2, 0)))
print()
#radi LineSegment

os = Oval(Point(10, 10), Point(8, 8))

print(os.getShapeName())

print(os.getBoundingBox().getX())
print(os.getBoundingBox().getY())
print(os.getBoundingBox().getWidth())
print(os.getBoundingBox().getHeight())

print(os.getHotPoint(0).getX())
print(os.getHotPoint(0).getY())
print(os.getHotPoint(1).getX())
print(os.getHotPoint(1).getY())

print(os.selectionDistance(Point(11, 11)))
#radi Oval