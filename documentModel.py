from __future__ import annotations
from typing import List, Optional
from point import Point
from graphicalObjectListener import GraphicalObjectListener
from graphicalObject import GraphicalObject
from rectangle import Rectangle
from documentModelListener import DocumentModelListener


class DocumentModel:
    SELECTION_PROXIMITY = 10.0

    def __init__(self):
        self.objects: List[GraphicalObject] = []
        self.roObjects: List[GraphicalObject] = self.objects[:]
        self.listeners: List[DocumentModelListener] = []
        self.selectedObjects: List[GraphicalObject] = []
        self.roSelectedObjects: List[GraphicalObject] = self.selectedObjects[:]

        self.goListener = self.GraphicalObjectListenerImpl(self)

    class GraphicalObjectListenerImpl(GraphicalObjectListener):
        def __init__(self, document_model: DocumentModel):
            self.document_model = document_model

        def graphicalObjectChanged(self, go: GraphicalObject) -> None:
            self.document_model.notifyListeners()

        def graphicalObjectSelectionChanged(self, go: GraphicalObject) -> None:
            if go.isSelected():
                if go not in self.document_model.selectedObjects:
                    self.document_model.selectedObjects.append(go)
            else:
                if go in self.document_model.selectedObjects:
                    self.document_model.selectedObjects.remove(go)
            self.document_model.notifyListeners()

    def clear(self) -> None:
        for obj in self.objects:
            obj.removeGraphicalObjectListener(self.goListener)
        self.objects.clear()
        self.selectedObjects.clear()
        self.notifyListeners()

    def addGraphicalObject(self, obj: GraphicalObject) -> None:
        if obj not in self.objects:
            self.objects.append(obj)
            obj.addGraphicalObjectListener(self.goListener)
            if obj.isSelected() and obj not in self.selectedObjects:
                self.selectedObjects.append(obj)
            self.notifyListeners()

    def removeGraphicalObject(self, obj: GraphicalObject) -> None:
        if obj in self.objects:
            self.objects.remove(obj)
            obj.removeGraphicalObjectListener(self.goListener)
            if obj in self.selectedObjects:
                self.selectedObjects.remove(obj)
            self.notifyListeners()

    def list(self) -> List[GraphicalObject]:
        return self.roObjects

    def addDocumentModelListener(self, listener: DocumentModelListener) -> None:
        if listener not in self.listeners:
            self.listeners.append(listener)

    def removeDocumentModelListener(self, listener: DocumentModelListener) -> None:
        if listener in self.listeners:
            self.listeners.remove(listener)

    def notifyListeners(self) -> None:
        for listener in self.listeners:
            listener.documentChanged()

    def getSelectedObjects(self) -> List[GraphicalObject]:
        return self.roSelectedObjects

    def increaseZ(self, go: GraphicalObject) -> None:
        index = self.objects.index(go)
        if index < len(self.objects) - 1:
            self.objects[index], self.objects[index + 1] = self.objects[index + 1], self.objects[index]
            self.notifyListeners()

    def decreaseZ(self, go: GraphicalObject) -> None:
        index = self.objects.index(go)
        if index > 0:
            self.objects[index], self.objects[index - 1] = self.objects[index - 1], self.objects[index]
            self.notifyListeners()

    def findSelectedGraphicalObject(self, mousePoint: Point) -> Optional[GraphicalObject]:
        closest_object = None
        closest_distance = self.SELECTION_PROXIMITY

        for obj in self.objects:
            distance = obj.selectionDistance(mousePoint)
            if distance < closest_distance:
                closest_distance = distance
                closest_object = obj

        return closest_object

    def findSelectedHotPoint(self, obj: GraphicalObject, mousePoint: Point) -> int:
        closest_index = -1
        closest_distance = self.SELECTION_PROXIMITY

        for i in range(obj.getNumberOfHotPoints()):
            distance = obj.getHotPointDistance(i, mousePoint)
            if distance < closest_distance:
                closest_distance = distance
                closest_index = i

        return closest_index