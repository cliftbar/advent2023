from dataclasses import dataclass
from pathlib import Path


@dataclass
class Card:
    card_id: int
    nums: set[int]
    matches: set[int]


def parse_cards(lines: list[str]) -> list[Card]:
    ret_cards: list[Card] = []
    for li in lines:
        id_part: str
        card_part: str
        id_part, card_part = li.split(": ")
        card_id: int = id_part[-1]

        num_section: str
        match_section: str
        num_section, match_section = card_part.split(" | ")

        nums: set[int] = set([int(n.strip()) for n in num_section.split(" ") if n])

        matches: set[int] = set([int(m.strip()) for m in match_section.strip().split(" ") if m])

        # print(nums)
        # print(matches)
        ret_cards.append(Card(card_id, nums, matches))
    return ret_cards


def card_game(lines: list[str]):
    cards: list[Card] = parse_cards(lines)

    total: int = 0

    for card in cards:
        intersection = card.nums.intersection(card.matches)
        count: int = len(intersection)
        points: int = 0 if count == 0 else 2 ** (max(count-1, 0))
        total += points

    print(total)



def main():
    ipt: Path = Path("../input.txt")
    with (ipt.open(mode="r") as input_fi):
        lines: list[str] = input_fi.readlines()

    card_game(lines)


if __name__ == "__main__":
    main()
