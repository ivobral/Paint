from state import State
from point import Point
from typing import List, Tuple
from graphicalObject import GraphicalObject
from renderer import Renderer
from lineSegment import LineSegment
from oval import Oval
import numpy as np

class EraserState(State):
    def __init__(self, model):
        self.model = model
        self.points: List[Point] = []
        self.threshold = 5.0  # Distance threshold for detecting close enough points

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
                if self.point_near_line(obj.hotPoints[0], line_start, line_end) or self.point_near_line(obj.hotPoints[1], line_start, line_end):
                    return True
        elif isinstance(obj, Oval):
            for i in range(len(self.points) - 1):
                line_start = self.points[i]
                line_end = self.points[i + 1]
                if self.line_intersects_oval(line_start, line_end, obj):
                    return True
        return False

    def line_intersects_oval(self, line_start: Point, line_end: Point, oval: Oval) -> bool:
        # Calculate the center, semi-major axis, and semi-minor axis
        h = (oval.hotPoints[0].x + oval.hotPoints[1].x) / 2
        k = (oval.hotPoints[0].y + oval.hotPoints[1].y) / 2
        a = abs(oval.hotPoints[0].x - oval.hotPoints[1].x) / 2
        b = abs(oval.hotPoints[0].y - oval.hotPoints[1].y) / 2

        # Sample points on the oval's boundary
        angles = np.linspace(0, 2 * np.pi, 300)  # Increased resolution
        points = [Point(h + a * np.cos(angle), k + b * np.sin(angle)) for angle in angles]

        # Check if any segment of the oval boundary intersects with the line
        for i in range(len(points) - 1):
            if self.do_lines_intersect(line_start, line_end, points[i], points[i + 1]):
                return True

        # Check last segment (closing the loop)
        if self.do_lines_intersect(line_start, line_end, points[-1], points[0]):
            return True

        # Additional check: If the line is within the oval
        if self.point_within_oval(line_start, oval) or self.point_within_oval(line_end, oval):
            return True

        return False

    def do_lines_intersect(self, line1_start: Point, line1_end: Point, line2_start: Point, line2_end: Point) -> bool:
        def orientation(p, q, r):
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if abs(val) < 1e-9:
                return 0  # collinear
            return 1 if val > 0 else 2  # clockwise or counterclockwise

        def on_segment(p, q, r):
            return (min(p.x, r.x) <= q.x <= max(p.x, r.x) and
                    min(p.y, r.y) <= q.y <= max(p.y, r.y))

        o1 = orientation(line1_start, line1_end, line2_start)
        o2 = orientation(line1_start, line1_end, line2_end)
        o3 = orientation(line2_start, line2_end, line1_start)
        o4 = orientation(line2_start, line2_end, line1_end)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special cases
        if (o1 == 0 and on_segment(line1_start, line2_start, line1_end)) or \
           (o2 == 0 and on_segment(line1_start, line2_end, line1_end)) or \
           (o3 == 0 and on_segment(line2_start, line1_start, line2_end)) or \
           (o4 == 0 and on_segment(line2_start, line1_end, line2_end)):
            return True

        return False

    def point_near_line(self, point: Point, line_start: Point, line_end: Point) -> bool:
        """ Check if a point is near a line segment within a threshold. """
        # Find the distance from point to the line segment
        if self.distance_from_line_segment(line_start, line_end, point) < self.threshold:
            return True
        return False

    def distance_from_line_segment(self, p1: Point, p2: Point, p: Point) -> float:
        """ Calculate the distance from a point to a line segment. """
        if p1 == p2:
            return self.distance(p1, p)
        
        # Projection of point p onto the line defined by p1 and p2
        line_mag = self.distance(p1, p2)
        u = ((p.x - p1.x) * (p2.x - p1.x) + (p.y - p1.y) * (p2.y - p1.y)) / (line_mag ** 2)
        if u < 0 or u > 1:
            # Closest point does not fall within the line segment
            return min(self.distance(p, p1), self.distance(p, p2))
        
        # Closest point falls within the line segment
        intersection = Point(p1.x + u * (p2.x - p1.x), p1.y + u * (p2.y - p1.y))
        return self.distance(p, intersection)

    def distance(self, p1: Point, p2: Point) -> float:
        """ Calculate Euclidean distance between two points. """
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

    def point_within_oval(self, point: Point, oval: Oval) -> bool:
        """ Check if a point is within an oval. """
        h = (oval.hotPoints[0].x + oval.hotPoints[1].x) / 2
        k = (oval.hotPoints[0].y + oval.hotPoints[1].y) / 2
        a = abs(oval.hotPoints[0].x - oval.hotPoints[1].x) / 2
        b = abs(oval.hotPoints[0].y - oval.hotPoints[1].y) / 2
        return ((point.x - h) ** 2) / (a ** 2) + ((point.y - k) ** 2) / (b ** 2) <= 1
