from __future__ import annotations
from abc import ABC, abstractmethod
from point import Point
from graphicalObjectListener import GraphicalObjectListener
from renderer import Renderer
from typing import List
from rectangle import Rectangle

class GraphicalObject(ABC):
    # Podrška za uređivanje objekta
    @abstractmethod
    def isSelected(self) -> bool:
        pass

    @abstractmethod
    def setSelected(self, selected: bool) -> None:
        pass

    @abstractmethod
    def getNumberOfHotPoints(self) -> int:
        pass

    @abstractmethod
    def getHotPoint(self, index: int) -> Point:
        pass

    @abstractmethod
    def setHotPoint(self, index: int, point: Point) -> None:
        pass

    @abstractmethod
    def isHotPointSelected(self, index: int) -> bool:
        pass

    @abstractmethod
    def setHotPointSelected(self, index: int, selected: bool) -> None:
        pass

    @abstractmethod
    def getHotPointDistance(self, index: int, mousePoint: Point) -> float:
        pass


    # Geometrijska operacija nad oblikom
    @abstractmethod
    def translate(self, delta: Point) -> None:
        pass
    
    @abstractmethod
    def getBoundingBox(self) -> Rectangle:
        pass

    @abstractmethod
    def selectionDistance(self, mousePoint: Point) -> float:
        pass

    # Podrška za crtanje (dio mosta)
    @abstractmethod
    def render(self, renderer: Renderer) -> None:
        pass

    # Observer za dojavu promjena modelu
    @abstractmethod
    def addGraphicalObjectListener(self, listener: GraphicalObjectListener) -> None:
        pass

    @abstractmethod
    def removeGraphicalObjectListener(self, listener: GraphicalObjectListener) -> None:
        pass

    # Podrška za prototip (alatna traka, stvaranje objekata u crtežu, ...)
    @abstractmethod
    def getShapeName(self) -> str:
        pass

    @abstractmethod
    def duplicate(self) -> GraphicalObject:
        pass

    
    # Podrška za snimanje i učitavanje
    @abstractmethod
    def getShapeID(self) -> str:
        pass

    @abstractmethod
    def load(self, stack: List[GraphicalObject], data: str) -> None:
        pass

    @abstractmethod
    def save(self, rows: List[str]) -> None:
        pass