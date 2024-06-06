#Napišite razred IdleState koji je implementacija sučelja state i u kojem su sve metode prazne.
from state import State
from point import Point
from renderer import Renderer
from graphicalObject import GraphicalObject

class IdleState(State):
    def __init__(self):
        print("IdleState")

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        print("mouseDown")

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        print("mouseUp")

    def mouseDragged(self, mousePoint: Point) -> None:
        print("mouseDragged")

    def keyPressed(self, keyCode: int) -> None:
        print("keyPressed")

    def afterDraw(self, r: Renderer, go: GraphicalObject) -> None:
        print("afterDraw")

    def afterDrawAll(self, r: Renderer) -> None:
        print("afterDrawAll")

    def onLeaving(self) -> None:
        print("onLeaving")