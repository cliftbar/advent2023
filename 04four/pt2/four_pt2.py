import sys
from dataclasses import dataclass
from pathlib import Path
from functools import wraps
from time import time


@dataclass
class Card:
    card_id: int
    nums: set[int]
    matches: set[int]

    def match_count(self) -> int:
        return len(self.nums.intersection(self.matches))


def parse_cards(lines: list[str]) -> dict[int, Card]:
    ret_cards: dict[int, Card] = {}
    for li in lines:
        id_part: str
        card_part: str
        id_part, card_part = li.split(": ")
        card_id: int = int(id_part.split(" ")[-1])

        num_section: str
        match_section: str
        num_section, match_section = card_part.split(" | ")

        nums: set[int] = set([int(n.strip()) for n in num_section.split(" ") if n])

        matches: set[int] = set([int(m.strip()) for m in match_section.strip().split(" ") if m])

        ret_cards[card_id] = Card(card_id, nums, matches)
    return ret_cards


# lol, this has been running for 12 hours
def card_game(lines: list[str]):
    cards: dict[int, Card] = parse_cards(lines)

    end_cards: list[Card] = list(cards.values())

    i: int = 0
    while True:
        card: Card = end_cards[i]
        end_cards = (end_cards[:i + 1]
                     + [cards[ci] for ci in range(card.card_id + 1, card.card_id + 1 + card.match_count())]
                     + end_cards[i + 1:])

        i += 1
        if len(end_cards) <= i:
            break
        if i % 10000 == 0:
            print(f"{len(end_cards)} {card.match_count()} {i}")

    print(len(end_cards))


# this one actually works
def card_game_two(lines: list[str]):
    cards: dict[int, Card] = parse_cards(lines)

    total = card_game_rec(list(cards.keys()), cards)
    print(total)


def card_game_rec(card_ids: list[int], originals: dict[int, Card]) -> int:
    if not card_ids:
        return 0
    card = card_ids[0]
    new_cards = []
    for ci in range(card, card + originals[card].match_count()):
        new_cards.append(originals[ci + 1].card_id)
    pass_card_ids = new_cards + card_ids[1:]
    return 1 + card_game_rec(pass_card_ids, originals)


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f"func: {f.__name__} args:[{args}, {kw}] took: {te - ts} sec")
        return result

    return wrap


@timing
def main():
    sys.setrecursionlimit(10000000)
    print(sys.getrecursionlimit())

    ipt: Path = Path("../input.txt")
    with (ipt.open(mode="r") as input_fi):
        lines: list[str] = input_fi.readlines()

    # card_game(lines)
    card_game_two(lines)

if __name__ == "__main__":
    main()
