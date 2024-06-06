from renderer import Renderer
from typing import List
from documentModel import DocumentModel
from point import Point
import tkinter as tk

class G2RendererImpl(Renderer):
    def __init__(self, documentModel: DocumentModel, canvas: tk.Canvas) -> None:
        self.documentModel = documentModel
        self.canvas = canvas

    def drawLine(self, s: Point, e: Point) -> None:
        # Postavi boju na plavu
		# Nacrtaj linijski segment od S do E
		# (sve to uporabom documentModel dobivenog u konstruktoru)
        self.canvas.create_line(s.x, s.y, e.x, e.y, fill="blue")

    def fillPolygon(self, points: List[Point]) -> None:
        # Postavi boju na plavu
		# Popuni poligon definiran danim točkama
		# Postavi boju na crvenu
		# Nacrtaj rub poligona definiranog danim točkama
		# (sve to uporabom documentModel dobivenog u konstruktoru)
        helpPoints = []
        for point in points:
            helpPoints.append(point.x)
            helpPoints.append(point.y)

        self.canvas.create_polygon(helpPoints, fill="blue", outline="red")