from ex3 import (
    CreatureFactory,
    FlameFactory,
    TransformCreatureFactory,
)


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def test_battle(first: CreatureFactory, second: CreatureFactory) -> None:
    print("Testing battle")
    creature1 = first.create_base()
    creature2 = second.create_base()
    print(creature1.describe())
    print(" vs.")
    print(creature2.describe())
    print(" fight!")
    print(creature1.attack())
    print(creature2.attack())


if __name__ == "__main__":
    test_factory(FlameFactory())
    print("\n")
    test_factory(TransformCreatureFactory())
    print("\n")
    test_battle(FlameFactory(), TransformCreatureFactory())