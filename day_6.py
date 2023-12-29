from collections.abc import Iterable
from functools import reduce
from operator import mul
import math


def parse_part_1(file_path: str) -> tuple[Iterable[int], Iterable[int]]:
    with open(file_path) as file:
        time_data = file.readline()
        distance_data = file.readline()
    return parse_numbers(time_data), parse_numbers(distance_data)


def parse_numbers(data: str) -> Iterable[int]:
    _, numbers = data.split(":")
    return tuple(int(n) for n in numbers.strip().split())


def solve_quadratic(a: int, b: int, c: int) -> tuple[float, float]:
    discriminant = (b ** 2) - (4 * a * c)  # assumes the discriminant is positive and there are two solutions
    solution_one = (-b + discriminant ** 0.5) / (2 * a)
    solution_two = (-b - discriminant ** 0.5) / (2 * a)
    return solution_one, solution_two


def ways_to_beat(time: int, distance: int) -> int:
    solutions = solve_quadratic(-1, time, -distance)
    solution_lower, solution_upper = solutions
    solution_lower = int(solution_lower) + 1 if solution_lower.is_integer() else math.ceil(solution_lower)
    solution_upper = int(solution_upper) - 1 if solution_upper.is_integer() else math.floor(solution_upper)
    return solution_upper - solution_lower + 1


def part_1(times: Iterable[int], distances: Iterable[int]) -> int:
    return reduce(mul, (ways_to_beat(time, distance) for time, distance in zip(times, distances)))


def parse_number(data: str) -> int:
    _, digits = data.replace(" ", "").split(":")
    return int(digits)


def parse_part_2(file_path: str) -> tuple[int, int]:
    with open(file_path) as file:
        time_data = file.readline()
        distance_data = file.readline()
    return parse_number(time_data), parse_number(distance_data)


if __name__ == "__main__":
    input_times, input_distances = parse_part_1("inputs/day_6.txt")
    print(part_1(input_times, input_distances))
    input_time, input_distance = parse_part_2("inputs/day_6.txt")
    print(part_1((input_time,), (input_distance,)))
