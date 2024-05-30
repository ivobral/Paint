from __future__ import annotations

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self) -> int:
        return self.x
    
    def getY(self) -> int:
        return self.y
    
    def translate(self, dp: Point) -> Point:
        return Point(self.getX() + dp.x, self.getY() + dp.y)
    
    def difference(self, p: Point) -> Point:
        return Point(self.getX() - p.x, self.getY() - p.y)