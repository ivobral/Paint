from graphicalObject import GraphicalObject
from typing import List
from graphicalObjectListener import GraphicalObjectListener
from point import Point
from abc import ABC, abstractmethod


class DocumentModelListener(ABC):
    @abstractmethod
    def documentChange(self):
        pass

class DocumentModel:
    SELECTION_PROXIMITY = 10
    
    def __init__(self):
        self.objects = []
        self.listeners = []
        self.selected_objects = []
    
    def clear(self):
        self.objects = []
        self.selected_objects = []
        self.notifyListeners()
    
    def addGraphicalObject(self, obj: GraphicalObject):
        self.objects.append(obj)
        obj.addGraphicalObjectListener(self.goListener)
        self.notifyListeners()
    
    def removeGraphicalObject(self, obj: GraphicalObject):
        if obj in self.objects:
            self.objects.remove(obj)
            obj.removeGraphicalObjectListener(self.goListener)
            self.selected_objects.remove(obj)
            self.notifyListeners()
    
    def list(self):
        return list(self.objects)
    
    def addDocumentModelListener(self, l: DocumentModelListener):
        self.listeners.append(l)
    
    def removeDocumentModelListener(self, l: DocumentModelListener):
        self.listeners.remove(l)
    
    def notifyListeners(self):
        for listener in self.listeners:
            listener.documentChange()
    
    def getSelectedObjects(self):
        return list(self.selected_objects)
    
    def increaseZ(self, go: GraphicalObject):
        if go in self.objects:
            index = self.objects.index(go)
            if index < len(self.objects) - 1:
                self.objects.remove(go)
                self.objects.insert(index + 1, go)
                self.notifyListeners()
    
    def decreaseZ(self, go: GraphicalObject):
        if go in self.objects:
            index = self.objects.index(go)
            if index > 0:
                self.objects.remove(go)
                self.objects.insert(index - 1, go)
                self.notifyListeners()
    
    def findSelectedGraphicalObject(self, mousePoint: Point):
        closest_object = None
        min_distance = float('inf')
        for obj in self.objects:
            distance = obj.selectionDistance(mousePoint)
            if distance < min_distance:
                closest_object = obj
                min_distance = distance
        if min_distance <= self.SELECTION_PROXIMITY:
            return closest_object
        else:
            return None
    
    def findSelectedHotPoint(self, obj: GraphicalObject, mousePoint: Point):
        # Implementacija pronalaženja selektiranog hot pointa
        pass