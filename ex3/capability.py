from abc import ABC, abstractmethod

class TransformCapability(ABC):
    def __init__(self):
        self._transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        """Switch to the transformed form, return a message."""

    @abstractmethod
    def revert(self) -> str:
        """Go back to the normal form, return a message."""
