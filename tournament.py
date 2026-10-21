from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    InvalidStrategyError,
)

# A type alias: a short name for a long type, to keep lines readable.
Opponent = tuple[CreatureFactory, BattleStrategy]


def label(opponent: Opponent) -> str:
    factory, strategy = opponent  # tuple unpacking
    name = factory.create_base().name
    # "AggressiveStrategy" -> "Aggressive"
    strat = type(strategy).__name__.replace("Strategy", "")
    return f"({name}+{strat})"


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    # Create each fighter ONCE, remember its strategy next to it.
    fighters = [(f.create_base(), s) for f, s in opponents]
    try:
        # Every pair once: j starts after i, so (A,B) but never (B,A)
        for i in range(len(fighters)):
            for j in range(i + 1, len(fighters)):
                first, first_strategy = fighters[i]
                second, second_strategy = fighters[j]
                print("\n* Battle *")
                print(first.describe())
                print(" vs.")
                print(second.describe())
                print(" now fight!")
                # The tournament never asks "which family?". It just
                # calls act(); each strategy decides what to do.
                for line in first_strategy.act(first):
                    print(line)
                for line in second_strategy.act(second):
                    print(line)
    except InvalidStrategyError as error:
        # abort the whole tournament on a bad creature/strategy pair
        print(f"Battle error, aborting tournament: {error}")


if __name__ == "__main__":
    flame = FlameFactory()
    shift = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    tournaments: list[tuple[str, list[Opponent]]] = [
        ("basic", [(flame, normal), (shift, aggressive)]),
        ("error", [(shift, aggressive), (flame, aggressive)]),
    ]
    for index, (title, opponents) in enumerate(tournaments):
        # enumerate gives (0, item), (1, item), ... : counter + value
        names = ", ".join(label(o) for o in opponents)
        print(f"\nTournament {index} ({title})")
        print(f" [ {names} ]")
        battle(opponents)