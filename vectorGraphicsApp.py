from tkinter import *

class VectorGraphicsApp(Canvas):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.root.title("Vector graphics app")
        self.focus_set()

        self.toolbar = Frame(self.root, bg="lightgrey", width = kwargs["width"], height = kwargs["height"])
        self.toolbar.pack(side=TOP, fill=X)

        self.load_button = Button(self.toolbar, text="Load", command="")
        self.load_button.pack(side=LEFT)

        self.save_button = Button(self.toolbar, text="Save", command="")
        self.save_button.pack(side=LEFT)

        self.svg_export_button = Button(self.toolbar, text="Export SVG", command="")
        self.svg_export_button.pack(side=LEFT)

        self.line_button = Button(self.toolbar, text="Line", command="")
        self.line_button.pack(side=LEFT)

        self.oval_button = Button(self.toolbar, text="Oval", command="")
        self.oval_button.pack(side=LEFT)

        self.select_button = Button(self.toolbar, text="Select", command="")
        self.select_button.pack(side=LEFT)

        self.eraser_button = Button(self.toolbar, text="Eraser", command="")
        self.eraser_button.pack(side=LEFT)

        self.cavas = Canvas(self.root, width=kwargs["width"], height=kwargs["height"])
        self.cavas.pack(fill=BOTH, expand=True)

        

