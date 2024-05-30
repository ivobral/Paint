class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getX(self) -> int:
        return self.x
    
    def getY(self) -> int:
        return self.y
    
    def getWidth(self) -> int:
        return self.width
    
    def getHeight(self) -> int:
        return self.height