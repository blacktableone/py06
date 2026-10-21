from abc import ABC, abstractmethod

class Creature(ABC):  #abstract: nobody can write Creature() directly
    def __init__(self, name: str, type: str) -> None:
        self.name = name  # attributes = data stored inside the object
        self.type = type

    @abstractmethod  # every child must write its own attack
    def attack(self) -> str:
        """"Return the attack message."""

    def describe(self)  -> str:  # concrete: children inherit it as-is
        return f"{self.name} is a {self.type} type Creature"


class Flameling(Creature):
    def __init__(self) -> None:
        # super().__init__ runs the PARENT's __init__ for us
        super().__init__("Flameling", "Fire")

    def attack(self):
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    def __init__(self):
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self):
        return f"{self.name} uses Flamethrower!"
