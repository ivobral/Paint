from GUI import GUI
from lineSegment import LineSegment
from oval import Oval

def main():
    objects = [LineSegment(), Oval()]

    GUI(objects, width=600, height=600)

if __name__ == "__main__":
    main()