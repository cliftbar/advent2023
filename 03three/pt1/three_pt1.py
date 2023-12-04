from dataclasses import dataclass
from pathlib import Path
import re
from re import Match

digits: list[str] = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9"
]


@dataclass
class Numbers:
    position: int
    len: int
    line: int
    value: int


@dataclass
class Symbols:
    position: int
    len: int
    line: int
    value: int


def parse_lines(lines: list[str]) -> (list[list[Match]], list[list[Match]]):
    total = "".join(lines)
    total = total.replace(".", "")
    total = total.replace("\n", "")
    for d in digits:
        total = total.replace(d, "")
    symbols: set = set(total)
    print(symbols)

    nums: list[list[Match]] = list()
    syms: list[list[Match]] = list()

    for li in lines:
        num_matches: list[Match[str]] = list(re.finditer("[0-9]+", li))
        nums.append([nm for nm in num_matches if nm.string])
        syms.append(list(re.finditer(f"[{''.join(symbols)}]+", li)))

    return nums, syms


def sym_search(num: Match, sym_up: list[Match], sym_on: list[Match], sym_below: list[Match]) -> bool:
    # print(num.start(), num.end())

    for sm in sym_up:
        if max(0, num.start() - 1) <= sm.start() and sm.end() <= num.end() + 1:
            return True

    for sm in sym_on:
        if sm.end() == num.start() or num.end() == sm.start():
            return True

    for sm in sym_below:
        if max(0, num.start() - 1) <= sm.start() and sm.end() <= num.end() + 1:
            return True

    return False


def schema(lines: list[str]):
    num_lines: list[list[Match]]
    sym_lines: list[list[Match]]
    num_lines, sym_lines = parse_lines(lines)

    total: int = 0
    for line_no in range(len(num_lines)):
        nl: list[Match] = num_lines[line_no]
        for num in nl:
            line_no_start: int = max(0, line_no - 1)
            line_no_end: int = min(len(num_lines) - 1, line_no + 1)
            if sym_search(num, sym_lines[line_no_start], sym_lines[line_no], sym_lines[line_no_end]):
                val = int(num.string[num.start():num.end()])
                print(val)
                total += val
            # break
    print(f"total: {total}")


def main():
    ipt: Path = Path("input.txt")
    with (ipt.open(mode="r") as input_fi):
        lines: list[str] = input_fi.readlines()

    schema(lines)


if __name__ == "__main__":
    main()
