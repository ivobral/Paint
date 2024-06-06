from state import State
from documentModel import DocumentModel
from graphicalObject import GraphicalObject
from point import Point

class AddShapeState(State):
    def __init__(self, model: DocumentModel, prototype: GraphicalObject):
        self.model: DocumentModel = model
        self.prototype: GraphicalObject = prototype

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        newObject = self.prototype.duplicate()
        newObject.translate(mousePoint)
        self.model.addGraphicalObject(newObject)

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        pass

    def mouseDragged(self, mousePoint: Point) -> None:
        pass

    def keyPressed(self, keyCode: int) -> None:
        pass

    def afterDraw(self, r, go) -> None:
        pass

    def afterDrawAll(self, r) -> None:
        pass

    def onLeaving(self) -> None:
        print("Leaving AddShapeState")

    