import math
from point import Point

class GeometryUtil:
    @staticmethod
    def distanceFromPoint(point1: Point, point2: Point) -> float:
        """Izračunaj euklidsku udaljenost između dvije točke."""
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
    
    @staticmethod
    def distanceFromLineSegment(s: Point, e: Point, p: Point) -> float:
        """
        Izračunaj koliko je točka P udaljena od linijskog segmenta određenog
        početnom točkom S i završnom točkom E.
        """

        # Ako je početna točka jednaka završnoj točki, onda je točka P udaljena
        # od linijskog segmenta jednako udaljena od te točke.
        if s.getX() == e.getX() and s.getY() == e.getY():
            return GeometryUtil.distanceFromPoint(s, p)

        # Vektor smjera linijskog segmenta
        v = e.difference(s)

        # Vektor od početne točke do točke P
        w = p.difference(s)

        # Projekcija vektora w na vektor v
        c1 = w.x * v.x + w.y * v.y
        c2 = v.x * v.x + v.y * v.y

        # Ako je točka P ispred početne točke, onda je najbliža točka
        # početna točka.
        if c1 <= 0:
            return GeometryUtil.distanceFromPoint(s, p)

        # Ako je točka P iza završne točke, onda je najbliža točka
        # završna točka.
        if c2 <= c1:
            return GeometryUtil.distanceFromPoint(e, p)

        # Projekcija vektora w na vektor v
        b = c1 / c2

        # Točka na linijskom segmentu koja je najbliža točki P
        pb = Point(s.x + b * v.x, s.y + b * v.y)

        # Udaljenost između točke P i točke na linijskom segmentu
        return GeometryUtil.distanceFromPoint(p, pb)