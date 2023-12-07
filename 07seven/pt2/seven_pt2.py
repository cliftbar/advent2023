from dataclasses import dataclass
from enum import Enum
from pathlib import Path

face_cards: dict[str, str] = {
    "T": "10",
    "Q": "11",
    "K": "12",
    "A": "13",
    "J": "1"
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

    @staticmethod
    def _is_full_house(hand_tokens: list[int], j_count: int) -> bool:
        if j_count == 0:
            return 2 in hand_tokens and 3 in hand_tokens
        if j_count == 1:
            return 2 == hand_tokens.count(2)
        elif j_count == 2:
            return 2 in hand_tokens and 1 in hand_tokens
        elif j_count == 3:
            raise Exception("Should have been a 4 of a kind")
        elif j_count == 4 or j_count == 5:
            raise Exception("Should have been a 5 of a kind")

    @staticmethod
    def _is_two_pair(hand_tokens: list[int], j_count: int) -> bool:
        if j_count == 0:
            return 2 == hand_tokens.count(2)
        if j_count == 1:
            return 2 in hand_tokens and 1 in hand_tokens
        elif j_count == 2:
            return 2 <= hand_tokens.count(1) or (2 in hand_tokens)
        elif j_count == 3:
            raise Exception("Should have been a 4 of a kind")
        elif j_count == 4 or j_count == 5:
            raise Exception("Should have been a 5 of a kind")

    @property
    def hand_dict(self):
        hand_dict: dict[int, int] = {}
        for c in self.cards:
            hand_dict[c] = hand_dict.get(c, 0) + 1
        return hand_dict

    @property
    def hand_type(self) -> HandType:
        # hand_tokens: list[int] = list({c: self.cards.count(c) for c in self.cards}.values())

        hand_dict = self.hand_dict

        j_count: int = hand_dict.pop(int(face_cards["J"]), 0)

        # card tokens without J's
        hand_tokens: list[int] = list(hand_dict.values())

        # just to determine basic counts, not complex cases (full house, two pair)
        hand_tokens_bumped = [t + j_count for t in hand_tokens]

        if 5 in hand_tokens_bumped or not hand_tokens:
            return HandType.FIVE
        elif 4 in hand_tokens_bumped:
            return HandType.FOUR
        elif self._is_full_house(hand_tokens, j_count):
            return HandType.FULL_HOUSE
        elif 3 in hand_tokens_bumped:
            return HandType.THREE
        elif self._is_two_pair(hand_tokens, j_count):
            return HandType.TWO_PAIR
        elif 2 in hand_tokens_bumped:
            return HandType.PAIR
        elif 1 in hand_tokens_bumped:
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

    [print(f"{h} {HandType(h.hand_type.value)} {h.hand_dict}") for h in ret_hands if 1 in h.cards]
    return ret_hands


def solution(lines: list[str]):
    hands: list[Hand] = parse_lines(lines)

    sorted_hands: list[Hand] = sorted(hands)
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
