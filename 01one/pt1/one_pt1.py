from pathlib import Path


def calibrate(cal_lines: list[str], print_line_cals: bool = False) -> int:

    nums_only: list[list[str]] = []
    for line in cal_lines:
        nums_only.append([c for c in line if c.isnumeric()])

    line_cals = [int(li[0] + li[-1]) for li in nums_only]

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
