#inerface for document model listener
from abc import ABC, abstractmethod

class DocumentModelListener(ABC):
    @abstractmethod
    def documentChanged(self) -> None:
        pass
