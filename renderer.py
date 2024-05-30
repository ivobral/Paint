from abc import ABC, abstractmethod
from typing import List
from point import Point

class Renderer(ABC):
    @abstractmethod
    def drawLine(self, s: Point, e: Point):
        pass
    
    @abstractmethod
    def fillPolygon(self, points: List[Point]):
        pass