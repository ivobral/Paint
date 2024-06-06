from __future__ import annotations
from tkinter import *
from typing import List
from graphicalObject import GraphicalObject
from documentModel import DocumentModel
from state import State
from idleState import IdleState
from G2RendererImpl import G2RendererImpl
from point import Point
from addShapeState import AddShapeState
from eraserState import EraserState
from documentModelListener import DocumentModelListener
from tkinter import filedialog
from svgRenederImpl import SVGRendererImpl
from lineSegment import LineSegment
from oval import Oval
from stack import Stack


class GUI(Tk):
    class DocumentModelListenerImpl(DocumentModelListener):
        def __init__(self, gui: GUI):
            self.gui = gui

        def documentChanged(self) -> None:
            self.gui.redraw()

    def __init__(self, objects: List[GraphicalObject], **kwargs) -> None:
        super().__init__()

        self.title("Vector graphics app")
        self.geometry(f"{kwargs['width']}x{kwargs['height']}")

        self.objects = objects
        self.documentModel = DocumentModel()
        self.documentModelListener = self.DocumentModelListenerImpl(self)
        self.documentModel.addDocumentModelListener(self.documentModelListener)

        self.currentSate: State = IdleState()

        self.bind("<KeyPress>", self.keyPressed)

        self.toolbar = Frame(self, bg="lightgrey", height=25, width=kwargs["width"])
        self.toolbar.pack(side=TOP, fill=X)

        self.load_button = Button(self.toolbar, text="Load", command=self.loadDrawing)
        self.load_button.pack(side=LEFT)

        self.save_button = Button(self.toolbar, text="Save", command=self.saveDrawing)
        self.save_button.pack(side=LEFT)

        self.svg_export_button = Button(self.toolbar, text="Export SVG", command=self.exportSVG)
        self.svg_export_button.pack(side=LEFT)

        for obj in self.objects:
            button = Button(self.toolbar, text=obj.getShapeName(), command=lambda obj=obj: self.setAddShapeState(obj))
            button.pack(side=LEFT)

        self.select_button = Button(self.toolbar, text="Select", command="")
        self.select_button.pack(side=LEFT)

        self.eraser_button = Button(self.toolbar, text="Eraser", command=self.setEraserState)
        self.eraser_button.pack(side=LEFT)

        self.canvas = Canvas(self, bg="lightyellow", width=kwargs["width"], height=kwargs["height"] - 25)
        self.canvas.pack(fill=BOTH, expand=True)
        self.renderer = G2RendererImpl(self.documentModel, self.canvas)

        self.canvas.bind("<Button-1>", self.mouseDown)
        self.canvas.bind("<ButtonRelease-1>", self.mouseUp)
        self.canvas.bind("<B1-Motion>", self.mouseDragged)

        self.mainloop()

    def loadDrawing(self) -> None:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            stack = Stack()
            prototype_map = {
                "@LINE": LineSegment(Point(0, 0), Point(0, 0)),
                "@OVAL": Oval(Point(0, 0), Point(0, 0)),
            }

            for line in lines:
                parts = line.split(maxsplit=1)
                shape_id = parts[0]
                data = parts[1] if len(parts) > 1 else ""
                prototype = prototype_map.get(shape_id)
                if prototype:
                    prototype.load(stack, data)
            
            self.documentModel.clear()
            while not stack.is_empty():
                self.documentModel.addGraphicalObject(stack.pop())
            self.redraw()

    def saveDrawing(self) -> None:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            rows = []
            for obj in self.documentModel.objects:
                obj.save(rows)
            with open(file_path, 'w') as f:
                f.write("\n".join(rows))

    def exportSVG(self) -> None:
        filePath = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG files", "*.svg")])
        if filePath:
            svgRenderer = SVGRendererImpl(filePath)
            for obj in self.documentModel.objects:
                obj.render(svgRenderer)
            svgRenderer.close()

    def setEraserState(self) -> None:
        self.currentSate.onLeaving()
        self.currentSate = EraserState(self.documentModel)
        print("EraserState")

    def setAddShapeState(self, obj: GraphicalObject) -> None:
        self.currentSate.onLeaving()
        self.currentSate = AddShapeState(self.documentModel, obj)
        print(f"AddShapeState: {obj.getShapeName()}")

    def is_canvas_event(self, event):
        return event.widget == self.canvas

    def mouseDown(self, event) -> None:
        if self.is_canvas_event(event):
            self.currentSate.mouseDown(Point(event.x, event.y), event.state & 1 << 0, event.state & 1 << 2)

    def mouseUp(self, event) -> None:
        if self.is_canvas_event(event):
            self.currentSate.mouseUp(Point(event.x, event.y), event.state & 1 << 0, event.state & 1 << 2)

    def mouseDragged(self, event) -> None:
        if self.is_canvas_event(event):
            self.currentSate.mouseDragged(Point(event.x, event.y))

    def keyPressed(self, event) -> None:
        if event.keysym == "Escape":
            self.currentSate.onLeaving()
            self.currentSate = IdleState()
        else:
            self.currentSate.keyPressed(event.keycode)

    def addObject(self, obj: GraphicalObject) -> None:
        new_obj = obj.duplicate()
        self.documentModel.addGraphicalObject(new_obj)
        self.redraw()

    def redraw(self) -> None:
        # Clear the canvas
        self.canvas.delete("all")

        for obj in self.documentModel.objects:
            obj.render(self.renderer)
            self.currentSate.afterDraw(self.renderer, obj)
        self.currentSate.afterDrawAll(self.renderer)
