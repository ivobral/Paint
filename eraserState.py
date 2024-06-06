from state import State
from point import Point
from typing import List
from graphicalObject import GraphicalObject
from renderer import Renderer
from lineSegment import LineSegment
from oval import Oval
from typing import Tuple

class EraserState(State):
    def __init__(self, model):
        self.model = model
        self.points: List[Point] = []

    def mouseDown(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        self.points = [mousePoint]

    def mouseUp(self, mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        self.points.append(mousePoint)
        self.eraseIntersectedObjects()
        self.points = []
        self.model.notifyListeners()

    def mouseDragged(self, mousePoint: Point) -> None:
        self.points.append(mousePoint)
        self.model.notifyListeners()  # Refresh the drawing to show the eraser line

    def keyPressed(self, keyCode: int) -> None:
        pass

    def afterDraw(self, r: Renderer, go: GraphicalObject) -> None:
        pass

    def afterDrawAll(self, r: Renderer) -> None:
        if len(self.points) > 1:
            for i in range(len(self.points) - 1):
                r.drawLine(self.points[i], self.points[i + 1])

    def onLeaving(self) -> None:
        self.points = []

    def eraseIntersectedObjects(self) -> None:
        for obj in self.model.objects:
            if self.intersects(obj):
                self.model.removeGraphicalObject(obj)


    def intersects(self, obj: GraphicalObject) -> bool:
        if isinstance(obj, LineSegment):
            for i in range(len(self.points) - 1):
                line_start = self.points[i]
                line_end = self.points[i + 1]
                if self.do_lines_intersect(line_start, line_end, obj.hotPoints[0], obj.hotPoints[1]):
                    return True
        elif isinstance(obj, Oval):
            for i in range(len(self.points) - 1):
                line_start = self.points[i]
                line_end = self.points[i + 1]
                for segment_start, segment_end in self.generate_oval_edges(obj):
                    if self.do_lines_intersect(line_start, line_end, segment_start, segment_end):
                        return True
        return False

    def generate_oval_edges(self, oval: Oval) -> List[Tuple[Point, Point]]:
        # Extract the vertices of the oval based on its bounding box
        bbox = oval.getBoundingBox()
        top_left = Point(bbox.x, bbox.y)
        top_right = Point(bbox.x + bbox.width, bbox.y)
        bottom_left = Point(bbox.x, bbox.y + bbox.height)
        bottom_right = Point(bbox.x + bbox.width, bbox.y + bbox.height)
        return [(top_left, top_right), (top_right, bottom_right), (bottom_right, bottom_left), (bottom_left, top_left)]

    def do_lines_intersect(self, line1_start: Point, line1_end: Point, line2_start: Point, line2_end: Point) -> bool:
        epsilon = 1e-9  # small value to handle floating-point precision issues

        def orientation(p, q, r):
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if abs(val) < epsilon:
                return 0  # collinear
            return 1 if val > 0 else 2  # clockwise or counterclockwise

        def on_segment(p, q, r):
            return (q.x <= max(p.x, r.x) + epsilon and q.x >= min(p.x, r.x) - epsilon and
                    q.y <= max(p.y, r.y) + epsilon and q.y >= min(p.y, r.y) - epsilon)

        o1 = orientation(line1_start, line1_end, line2_start)
        o2 = orientation(line1_start, line1_end, line2_end)
        o3 = orientation(line2_start, line2_end, line1_start)
        o4 = orientation(line2_start, line2_end, line1_end)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special cases (collinear cases)
        if (o1 == 0 and on_segment(line1_start, line2_start, line1_end)) or \
                (o2 == 0 and on_segment(line1_start, line2_end, line1_end)) or \
                (o3 == 0 and on_segment(line2_start, line1_start, line2_end)) or \
                (o4 == 0 and on_segment(line2_start, line1_end, line2_end)):
            return True

        return False