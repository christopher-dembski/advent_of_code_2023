from typing import NamedTuple


class ScratchCard(NamedTuple):
    winning_numbers: frozenset[int, ...]
    chosen_numbers: frozenset[int, ...]


def parse_input(file_path: str) -> tuple[ScratchCard, ...]:
    scratch_cards = []
    with open(file_path) as file:
        lines = file.read().strip().split("\n")
    for line in lines:
        _, data = line.split(":")
        winning_numbers, chosen_numbers = data.split("|")
        winning_numbers = frozenset(int(n) for n in winning_numbers.strip().split())
        chosen_numbers = frozenset(int(n) for n in chosen_numbers.strip().split())
        scratch_cards.append(ScratchCard(winning_numbers, chosen_numbers))
    return tuple(scratch_cards)


def score(scratch_card: ScratchCard) -> int:
    winning_numbers_selected = scratch_card.winning_numbers & scratch_card.chosen_numbers
    return 2 ** (len(winning_numbers_selected) - 1) if winning_numbers_selected else 0


def part_1(scratch_cards: tuple[ScratchCard, ...]) -> int:
    return sum(score(scratch_card) for scratch_card in scratch_cards)


def calculate_number_won(card_number: int, scratch_cards: tuple[ScratchCard, ...]) -> int:
    scratch_card = scratch_cards[card_number]
    num_cards_won = len(scratch_card.winning_numbers & scratch_card.chosen_numbers)
    card_numbers_won = range(card_number + 1, card_number + 1 + num_cards_won)
    return 1 + sum(calculate_number_won(n, scratch_cards) for n in card_numbers_won)


def part_2(scratch_cards: tuple[ScratchCard, ...]) -> int:
    return sum(calculate_number_won(n, scratch_cards) for n in range(len(scratch_cards)))


if __name__ == "__main__":
    test_scratch_cards = parse_input("inputs/day_4.txt")
    print(part_2(test_scratch_cards))
