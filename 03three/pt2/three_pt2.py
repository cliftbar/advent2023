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


def match_val(m: Match) -> str:
    return m.string[m.start():m.end()]


def parse_lines(lines: list[str]) -> (list[list[Match]], list[list[Match]]):
    nums: list[list[Match]] = list()
    syms: list[list[Match]] = list()

    for li in lines:
        num_matches: list[Match[str]] = list(re.finditer("[0-9]+", li))
        nums.append([nm for nm in num_matches if nm.string])
        syms.append(list(re.finditer("[*]+", li)))

    return nums, syms


def gear_search(sym: Match, num_up: list[Match], num_on: list[Match], num_below: list[Match]) -> int:
    num_found: list[Match] = list()

    for nm in num_up:
        if max(0, nm.start() - 1) <= sym.start() and sym.end() <= nm.end() + 1:
            num_found.append(nm)

    for nm in num_on:
        if sym.end() == nm.start() or nm.end() == sym.start():
            num_found.append(nm)

    for nm in num_below:
        if max(0, nm.start() - 1) <= sym.start() and sym.end() <= nm.end() + 1:
            num_found.append(nm)

    return 0 if len(num_found) != 2 else int(match_val(num_found[0])) * int(match_val(num_found[1]))


def schema(lines: list[str]):
    num_lines: list[list[Match]]
    sym_lines: list[list[Match]]
    num_lines, sym_lines = parse_lines(lines)

    total: int = 0
    for line_no in range(len(sym_lines)):
        sl: list[Match] = sym_lines[line_no]
        for sym in sl:
            line_no_start: int = max(0, line_no - 1)
            line_no_end: int = min(len(num_lines) - 1, line_no + 1)
            total += gear_search(sym, num_lines[line_no_start], num_lines[line_no], num_lines[line_no_end])
            # break
    print(f"total: {total}")


def main():
    ipt: Path = Path("input.txt")
    with (ipt.open(mode="r") as input_fi):
        lines: list[str] = input_fi.readlines()

    schema(lines)


if __name__ == "__main__":
    main()
