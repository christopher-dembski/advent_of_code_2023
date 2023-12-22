from typing import TypeAlias, NamedTuple

Schematic: TypeAlias = tuple[tuple[str, ...]]
Position: TypeAlias = tuple[int, int]


class PartNumber(NamedTuple):
    value: int
    positions: tuple[Position]


def parse_input(file_path: str) -> Schematic:
    with open(file_path) as file:
        return tuple(tuple(ch for ch in row) for row in file.read().split("\n"))


def get_part_numbers_and_part_positions(schematic: Schematic) -> tuple[set[PartNumber], set[Position]]:
    part_numbers: set[PartNumber] = set()
    part_positions: set[Position] = set()

    for r, row in enumerate(schematic):
        for c, ch in enumerate(row):
            if is_start_of_number(r, c, schematic):
                part_numbers.add(parse_part_number(r, c, schematic))
            elif is_part(schematic[r][c]):
                part_positions.add((r, c))
    return part_numbers, part_positions


def is_part(ch: str) -> bool:
    return not (ch.isdigit() or ch == ".")


def is_start_of_number(r: int, c: int, schematic: Schematic) -> bool:
    return schematic[r][c].isdigit() and (c == 0 or not schematic[r][c - 1].isdigit())


def parse_part_number(r: int, c: int, schematic: Schematic) -> PartNumber:
    value = ""
    positions: set[Position] = set()
    while c < len(schematic[0]) and schematic[r][c].isdigit():
        value += schematic[r][c]
        positions.add((r, c))
        c += 1
    return PartNumber(int(value), tuple(positions))


def adjacent_positions_to_part_number(part_number: PartNumber, schematic: Schematic) -> set[Position]:
    adjacent: set[Position] = set()
    for r, c in part_number.positions:
        adjacent |= {(r - 1, c), (r - 1, c + 1), (r, c + 1), (r + 1, c + 1),
                     (r + 1, c), (r + 1, c - 1), (r, c - 1), (r - 1, c - 1)}
    return {(r, c) for r, c in adjacent if 0 <= r < len(schematic) and 0 <= c < len(schematic[0])}


def adjacent_to_part(part_number: PartNumber, part_positions: set[Position], schematic: Schematic) -> bool:
    return any(position in part_positions for position in adjacent_positions_to_part_number(part_number, schematic))


def get_adjacent_part_numbers(position: Position, part_numbers: set[PartNumber], schematic: Schematic
                              ) -> tuple[PartNumber, ...]:
    return tuple(part_number for part_number in part_numbers
                 if position in adjacent_positions_to_part_number(part_number, schematic))


def part_1(schematic: Schematic) -> int:
    part_numbers, part_positions = get_part_numbers_and_part_positions(schematic)
    return sum(part_number.value for part_number in part_numbers
               if adjacent_to_part(part_number, part_positions, schematic))


def part_2(schematic: Schematic) -> int:
    part_numbers, part_positions = get_part_numbers_and_part_positions(schematic)
    gear_positions = {(r, c) for r, c in part_positions if schematic[r][c] == "*"}
    total = 0
    for position in gear_positions:
        adjacent_part_numbers: tuple[PartNumber] = get_adjacent_part_numbers(position, part_numbers, schematic)
        if len(adjacent_part_numbers) == 2:
            total += adjacent_part_numbers[0].value * adjacent_part_numbers[1].value
    return total


if __name__ == "__main__":
    test_schematic = parse_input("inputs/day_3_ex.txt")
    print(part_2(test_schematic))
