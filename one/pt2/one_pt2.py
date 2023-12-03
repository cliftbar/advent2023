import re
from pathlib import Path


to_digit: dict[str, str] = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9"
}

words_and_digits: list[str] = [
    "zero",
    "0",
    "one",
    "1",
    "two",
    "2",
    "three",
    "3",
    "four",
    "4",
    "five",
    "5",
    "six",
    "6",
    "seven",
    "7",
    "eight",
    "8",
    "nine",
    "9"
]


def calibrate(cal_lines: list[str], print_line_cals: bool = False) -> int:
    line_cals: list[int] = list()

    for line in cal_lines:

        idx_map: dict[int, str] = dict()
        for v in words_and_digits:
            if v in line:
                first: int = line.find(v)
                last: int = line.rfind(v)
                idx_map[first] = to_digit[v]
                idx_map[last] = to_digit[v]

        print(idx_map)
        sorted_keys: list[int] = sorted(list(idx_map.keys()))
        line_cals.append(int(idx_map[sorted_keys[0]] + idx_map[sorted_keys[-1]]))

    if print_line_cals:
        for cal in line_cals:
            print(cal)

    return sum(line_cals)


def main():
    ipt: Path = Path("input.txt")
    with (ipt.open(mode="r") as input_fi):
        lines: list[str] = input_fi.readlines()

    calibation_value: int = calibrate(lines, True)
    print(calibation_value)


if __name__ == "__main__":
    main()
