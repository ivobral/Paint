from abc import ABC, abstractmethod

class GraphicalObjectListener(ABC):
    @abstractmethod
    def graphicalObjectChanged(self, go) -> None:
        pass

    @abstractmethod
    def graphicalObjectSelectionChanged(self, go) -> None:
        pass