from abc import ABC, abstractmethod
from point import Point
from renderer import Renderer
from graphicalObject import GraphicalObject

class State(ABC):
    @abstractmethod
    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        pass

    @abstractmethod
    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        pass

    @abstractmethod
    def mouseDragged(self, mousePoint: Point) -> None:
        pass

    @abstractmethod
    def keyPressed(self, keyCode: int) -> None:
        pass

    @abstractmethod
    def afterDraw(self, r: Renderer, go: GraphicalObject) -> None:
        pass

    @abstractmethod
    def afterDrawAll(self, r: Renderer) -> None:
        pass

    @abstractmethod
    def onLeaving(self) -> None:
        pass