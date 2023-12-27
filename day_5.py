import re


class Map:

    def __init__(self, ranges: tuple[tuple[int, int, int], ...]):
        self.source_ranges = tuple(range(source_start, source_start + length)
                                   for destination_start, source_start, length in ranges)
        self.conversion_rates = tuple(destination_start - source_start
                                      for destination_start, source_start, _ in ranges)

    def convert(self, n: int) -> int:
        for rng, conversion_rate in zip(self.source_ranges, self.conversion_rates):
            if n in rng:
                return n + conversion_rate
        return n

    def __repr__(self):
        ranges = (f"Range(start={rng.start}, stop={rng.stop}, conversion_rate={conversion_rate})"
                  for rng, conversion_rate in zip(self.source_ranges, self.conversion_rates))
        return f"Map({', '.join(ranges)})"


def parse(file_path: str) -> tuple[tuple[int, ...], tuple[Map, ...]]:
    with open(file_path) as file:
        data = file.read()
    sections = re.split(r"\n\s+", data, re.MULTILINE)
    seeds = parse_seeds_data(sections[0])
    maps = tuple(parse_map(section) for section in sections[1::])
    return seeds, maps


def parse_map(data: str) -> Map:
    _, numbers = data.split(":\n")
    ranges_data = tuple(tuple(int(n) for n in line.split()) for line in numbers.strip().split("\n"))
    return Map(ranges_data)  # type: ignore


def parse_seeds_data(data: str) -> tuple[int, ...]:
    _, numbers = data.split(":")
    return tuple(int(n) for n in numbers.strip().split())


def calculate_location_number(n: int, maps: tuple[Map, ...]) -> int:
    for mp in maps:
        n = mp.convert(n)
    return n


def part_1(seeds: tuple[int, ...], maps: tuple[Map, ...]) -> int:
    return min(calculate_location_number(seed, maps) for seed in seeds)


if __name__ == "__main__":
    test_seeds, test_maps = parse("inputs/day_5.txt")
    print(part_1(test_seeds, test_maps))
