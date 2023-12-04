from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Colors(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


target: dict[Colors, int] = {
    Colors.RED: 12,
    Colors.GREEN: 13,
    Colors.BLUE: 14
}


@dataclass
class GameLine:
    game_id: int
    max_red: int
    max_green: int
    max_blue: int


def parse_game_line(li: str) -> GameLine:
    game_id_part: str
    round_part: str
    game_id_part, round_part = li.split(":")

    game_id: str = int(game_id_part.split(" ")[1].strip())

    rounds: list[str] = [rp.strip() for rp in round_part.split(";")]
    round_maxes: dict[Colors, int] = dict()
    for r in rounds:
        colors: list[str] = [c.strip() for c in r.split(",")]

        for cl in colors:
            num, color = cl.split(" ")
            round_maxes[Colors(color)] = max(int(num), round_maxes.get(Colors(color), 0))
    return GameLine(game_id, round_maxes[Colors.RED], round_maxes[Colors.GREEN], round_maxes[Colors.BLUE])


def is_possible(game_line: GameLine) -> bool:
    return (game_line.max_red <= target[Colors.RED] and game_line.max_green <= target[Colors.GREEN]
            and game_line.max_blue <= target[Colors.BLUE])


def game(game_lines: list[str]) -> int:
    games: list[GameLine] = [parse_game_line(gl) for gl in game_lines]
    possible_games: list[GameLine] = [g for g in games if is_possible(g)]

    # print(possible_games)
    print(sum([g.game_id for g in possible_games]))


def main():
    ipt: Path = Path("input.txt")
    with (ipt.open(mode="r") as input_fi):
        lines: list[str] = input_fi.readlines()

    game(lines)


if __name__ == "__main__":
    main()
