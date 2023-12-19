from typing import TypeAlias
from functools import reduce
from operator import mul

Draw = tuple[int, str]
Round: TypeAlias = tuple[Draw]
Game: TypeAlias = tuple[Round]


def parse_input(file_path: str) -> tuple[Game, ...]:
    with open(file_path) as file:
        lines = file.read().strip().split("\n")
    games = [data.strip() for title, data in (line.split(":") for line in lines)]
    parsed = [[] for _ in games]
    for i, game in enumerate(games):
        rounds = game.split(";")
        for rnd in rounds:
            numbers_and_colors = (st.strip().split(" ") for st in rnd.split(","))
            parsed_round = tuple((int(n), color) for n, color in numbers_and_colors)
            parsed[i].append(parsed_round)
    return tuple(tuple(game) for game in parsed)  # type: ignore


def possible_game(game: Game, bag: dict[str, int]) -> bool:
    return all(possible_set(st, bag) for st in game)


def possible_set(rnd: Round, bag: dict[str, int]) -> bool:
    totals = {color: 0 for color in bag}
    for n, color in rnd:
        totals[color] += n
    return all(n <= bag[color] for color, n in totals.items())


def part_1(games: tuple[Game], bag: dict[str: int]) -> int:
    return sum(i + 1 for i, game in enumerate(games) if possible_game(game, bag))


def get_totals(rnd: Round) -> dict[str, int]:
    totals = {}
    for n, color in rnd:
        totals[color] = totals.get(color, 0) + n
    return totals


def get_minimums(game: Game, colors: tuple[str]) -> dict[str: int]:
    minimums = {color: 0 for color in colors}
    for st in game:
        totals = get_totals(st)
        for color, n in totals.items():
            if n > minimums.get(color, 0):
                minimums[color] = n
    return minimums


def part_2(games: tuple[Game, ...], colors=("red", "green", "blue")) -> int:
    return sum(reduce(mul, minimums) for minimums in (get_minimums(game, colors).values() for game in games))


if __name__ == "__main__":
    test_data = parse_input("inputs/day_2.txt")
    test_bag = {"red": 12, "green": 13, "blue": 14}
    print(part_1(test_data, test_bag))
