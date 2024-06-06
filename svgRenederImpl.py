from renderer import Renderer
from point import Point
from typing import List

class SVGRendererImpl(Renderer):
    def __init__(self, fileName: str):
        self.lines = []
        self.fileName = fileName
        self.lines.append('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">')

    def drawLine(self, s: Point, e: Point) -> None:
        self.lines.append(f'<line x1="{s.x}" y1="{s.y}" x2="{e.x}" y2="{e.y}" style="stroke:rgb(0,0,255);stroke-width:1" />')

    def fillPolygon(self, points: List[Point]) -> None:
        self.lines.append('<polygon points="')
        for point in points:
            self.lines.append(f'{point.x},{point.y} ')
        self.lines.append('" style="fill:blue;stroke:red;stroke-width:1" />')

    def close(self) -> None:
        self.lines.append('</svg>')
        with open(self.fileName, 'w') as f:
            f.write("\n".join(self.lines))

