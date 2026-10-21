from ex3 import Creature, TransformCapability, TransformCreatureFactory


def test_transform(creature: Creature) -> None:
    print(creature.describe())
    print(creature.attack())
    # isinstance asks: "does this creature ALSO have the ability?"
    # Inside the if, mypy knows transform/revert exist.
    if isinstance(creature, TransformCapability):
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
    else:
        print(f"{creature.name} cannot transform")


if __name__ == "__main__":
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()
    print(" base:")
    test_transform(factory.create_base())
    print(" evolved:")
    test_transform(factory.create_evolved())