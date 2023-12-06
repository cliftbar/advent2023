from dataclasses import dataclass
from functools import reduce
from pathlib import Path


def parse_lines(lines: list[str]) -> (list[int], list[int]):
    times: list[int] = [int(v.strip()) for v in lines[0].split(":")[1].strip().split(" ") if v]
    dist: list[int] = [int(v.strip()) for v in lines[1].split(":")[1].strip().split(" ") if v]

    print(times, dist)
    return times, dist


def solution(lines: list[str]):
    times: list[int]
    dist: list[int]

    times, dist = parse_lines(lines)

    times = [int("".join([str(t) for t in times]))]
    dist = [int("".join([str(d) for d in dist]))]

    race_opts: list[int] = []
    for race_iter in range(len(times)):
        race_time: int = times[race_iter]
        dist_record: int = dist[race_iter]
        opts: int = 0
        for hold_time in range(race_time):
            travel_dist: int = (race_time * hold_time) - (hold_time * hold_time)
            if dist_record < travel_dist:
                opts += 1

        print(opts)
        race_opts.append(opts)
    print(race_opts)
    print(reduce(lambda x, y: x * y, race_opts))


def main():
    # ipt: Path = Path("../sample_input.txt")
    ipt: Path = Path("../input.txt")
    with (ipt.open(mode="r") as input_fi):
        lines: list[str] = input_fi.readlines()

    solution(lines)


if __name__ == "__main__":
    main()
