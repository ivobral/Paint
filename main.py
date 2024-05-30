from tkinter import *
from vectorGraphicsApp import VectorGraphicsApp

def main():
    root = Tk()
    app = VectorGraphicsApp(root, width=800, height=600, bg="white")
    root.mainloop()

if __name__ == "__main__":
    main()