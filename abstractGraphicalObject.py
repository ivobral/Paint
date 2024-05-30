from graphicalObject import GraphicalObject
from graphicalObjectListener import GraphicalObjectListener
from geometryUtil import GeometryUtil
from point import Point
from typing import List

class AbstractGraphicalObject(GraphicalObject):
    def __init__(self, points: List[Point]):
        self.hotPoints = points
        self.hotPointSelected = [False] * len(points)
        self.selected = False
        self.listeners = List[GraphicalObjectListener]

    def addGraphicalObjectListener(self, listener: GraphicalObjectListener) -> None:
        self.listeners.append(listener)

    def removeGraphicalObjectListener(self, listener: GraphicalObjectListener) -> None:
        self.listeners.remove(listener)

    def notifyListeners(self) -> None:
        for listener in self.listeners:
            listener.graphicalObjectChanged(self)

    def notifySelectionListeners(self) -> None:
        for listener in self.listeners:
            listener.graphicalObjectSelectionChanged(self)

    def isSelected(self) -> bool:
        return self.selected
    
    def setSelected(self, selected: bool) -> None:
        self.selected = selected
        self.notifySelectionListeners()
        self.notifyListeners()

    def getNumberOfHotPoints(self) -> int:
        return len(self.hotPoints)
    
    def getHotPoint(self, index: int) -> Point:
        return self.hotPoints[index]
    
    def setHotPoint(self, index: int, point: Point) -> None:
        self.hotPoints[index] = point
        self.notifyListeners()

    def setHotPointSelected(self, index: int, selected: bool) -> None:
        self.hotPointSelected[index] = selected
        self.notifyListeners()

    def getHotPointDistance(self, index: int, mousePoint: Point) -> float:
        return GeometryUtil.distanceFromPoint(self.hotPoints[index], mousePoint)
    
    def translate(self, delta: Point) -> None:
        for i in range(len(self.hotPoints)):
            self.hotPoints[i] = self.hotPoints[i].translate(delta)
        self.notifyListeners()

    def isHotPointSelected(self, index: int) -> bool:
        return self.hotPointSelected[index]