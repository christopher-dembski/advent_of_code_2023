NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def parse_input(file_path: str) -> tuple[str, ...]:
    with open(file_path) as file:
        return tuple(file.read().splitlines())


def part_1(lines: tuple[str, ...]):
    total = 0
    for line in lines:
        for ch in line:
            if ch.isdigit():
                total += int(ch) * 10
                break
        for ch in reversed(line):
            if ch.isdigit():
                total += int(ch)
                break
    return total


def part_2(lines: tuple[str, ...]):
    total = 0
    for line in lines:
        for i in range(len(line)):
            if n := get_digit(line, i):
                total += n * 10
                break
        for i in range(len(line) - 1, -1, -1):
            if n := get_digit(line, i):
                total += n
                break
    return total


def get_digit(line: str, i: int) -> int | None:
    ch = line[i]
    if ch.isdigit():
        return int(ch)
    for length in range(3, 6):
        if n := NUMBERS.get(line[i:i + length], None):
            return n


if __name__ == "__main__":
    parsed_input = parse_input("inputs/day_1.txt")
    print(part_2(parsed_input))
