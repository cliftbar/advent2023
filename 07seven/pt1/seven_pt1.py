from dataclasses import dataclass
from enum import Enum
from pathlib import Path

face_cards: dict[str, str] = {
    "T": "10",
    "J": "11",
    "Q": "12",
    "K": "13",
    "A": "14",
}


class HandType(Enum):
    FIVE = 1
    FOUR = 2
    FULL_HOUSE = 3
    THREE = 4
    TWO_PAIR = 5
    PAIR = 6
    ONE = 7
    HIGH = 8


@dataclass
class Hand:
    cards: list[int]
    bid: int

    @property
    def hand_type(self) -> HandType:
        # hand_tokens: list[int] = list({c: self.cards.count(c) for c in self.cards}.values())
        hand_dict: dict[int, int] = {}
        for c in self.cards:
            hand_dict[c] = hand_dict.get(c, 0) + 1
        hand_tokens: list[int] = list(hand_dict.values())
        if 5 in hand_tokens:
            return HandType.FIVE
        elif 4 in hand_tokens:
            return HandType.FOUR
        elif 3 in hand_tokens and 2 in hand_tokens:
            return HandType.FULL_HOUSE
        elif 3 in hand_tokens:
            return HandType.THREE
        elif 2 == hand_tokens.count(2):
            return HandType.TWO_PAIR
        elif 2 in hand_tokens:
            return HandType.PAIR
        elif 1 in hand_tokens:
            return HandType.ONE
        else:
            return HandType.HIGH

    @staticmethod
    def from_line(line: str) -> "Hand":
        card_str: str
        bid: str
        card_str, bid = line.split(" ")
        return Hand([int(face_cards.get(c, c)) for c in card_str], int(bid))

    def result(self, round_rank: int) -> int:
        return self.bid * round_rank

    def __eq__(self, other: "Hand") -> bool:
        return self.cards == other.cards

    def __lt__(self, other: "Hand") -> bool:
        if other.hand_type.value < self.hand_type.value:
            return True
        elif self.hand_type.value < other.hand_type.value:
            return False

        for i in range(len(self.cards)):
            if self.cards[i] < other.cards[i]:
                return True
            elif other.cards[i] < self.cards[i]:
                return False

        return False

    def __gt__(self, other: "Hand") -> bool:
        if other.hand_type.value < self.hand_type.value:
            return True
        elif self.hand_type.value < other.hand_type.value:
            return False

        for i in range(len(self.cards)):
            if self.cards[i] < other.cards[i]:
                return True
            elif other.cards[i] < self.cards[i]:
                return False

        return False


def parse_lines(lines: list[str]) -> (list[int], list[int]):
    ret_hands: list[Hand] = []
    for l in lines:
        ret_hands.append(Hand.from_line(l))

    print([f"{h} {h.hand_type.value}" for h in ret_hands])
    return ret_hands


def solution(lines: list[str]):
    hands: list[Hand] = parse_lines(lines)

    sorted_hands: list[Hand] = sorted(hands)
    print([f"{h} {h.hand_type}" for h in sorted_hands])
    total: int = 0
    for i in range(len(sorted_hands)):
        total += sorted_hands[i].bid * (i + 1)

    print(total)


def main():
    # ipt: Path = Path("../sample_input.txt")
    ipt: Path = Path("../input.txt")
    with (ipt.open(mode="r") as input_fi):
        lines: list[str] = input_fi.readlines()

    solution(lines)


if __name__ == "__main__":
    main()
