from abc import ABC, abstractmethod
from .creature import Creature, Flameling, Pyrodon
from .shapeshifters import Shiftling, Morphagon


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        """Create the basic creature of this family."""

    def create_evolved(self) -> Creature:
        """Create the evolved creature of this family."""

class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        # returns a Creature; caller never sees
        # the concrete class name
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Shiftling()

    def create_evolved(self) -> Creature:
        return Morphagon()
