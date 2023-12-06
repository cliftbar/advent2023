from dataclasses import dataclass
from pathlib import Path


@dataclass
class Ranger:
    source: int
    dest: int
    step: int

    @staticmethod
    def from_line(line: str) -> "Ranger":
        d, s, step = line.strip(".").split(" ")
        return Ranger(int(s), int(d), int(step))


def parse_lines_bigrange(lines: list[str]) -> (dict[str, dict[int, int]], list[int]):
    sections: list[str] = ".".join(lines).split(".\n")

    seeds: list[int] = list(map(int, sections[0].split(": ")[1].split(" ")))
    print(seeds)

    ret_map: dict[str, dict[int, int]] = {}
    for sec in sections[1:]:
        sec_lines = sec.strip().strip(".").split("\n")
        map_type: str = sec_lines[0][:-1]
        # print(map_type)

        range_dict: dict[int, int] = {}
        for sl in sec_lines[1:]:
            r = Ranger.from_line(sl.strip("."))
            for i in range(r.step):
                range_dict[r.source + i] = r.dest + i

        # print(range_dict)
        ret_map[map_type] = range_dict

    return ret_map, seeds


# lol, memory error this time
def solution_bigrange(lines: list[str]):
    maps: dict[str, dict[int, int]]
    seeds: list[int]
    maps, seeds = parse_lines_bigrange(lines)

    min_loc = float("inf")
    for seed in seeds:
        s2s: int = maps["seed-to-soil map"].get(seed, seed)
        s2f: int = maps["soil-to-fertilizer map"].get(s2s, s2s)
        f2w: int = maps["fertilizer-to-water map"].get(s2f, s2f)
        w2li: int = maps["water-to-light map"].get(f2w, f2w)
        li2t: int = maps["light-to-temperature map"].get(w2li, w2li)
        t2h: int = maps["temperature-to-humidity map"].get(li2t, li2t)
        htlo: int = maps["humidity-to-location map"].get(t2h, t2h)

        min_loc = min(min_loc, htlo)
        print(f"{seed} {min_loc}")
    print(min_loc)


def parse_lines(lines: list[str]) -> (dict[str, list[Ranger]], list[int]):
    sections: list[str] = ".".join(lines).split(".\n")

    seeds: list[int] = list(map(int, sections[0].split(": ")[1].split(" ")))
    print(seeds)

    ret_map: dict[str, list[Ranger]] = {}
    for sec in sections[1:]:
        sec_lines = sec.strip().strip(".").split("\n")
        map_type: str = sec_lines[0][:-1]
        # print(map_type)

        range_list: list[Ranger] = []
        for sl in sec_lines[1:]:
            r = Ranger.from_line(sl.strip("."))
            range_list.append(r)

        # print(range_dict)
        ret_map[map_type] = range_list

    return ret_map, seeds


def source_to_dest(source: int, ranges: list[Ranger]):
    for r in ranges:
        if r.source <= source < r.source + r.step:
            return r.dest + (source - r.source)

    return source


def solution(lines: list[str]):
    maps: dict[str, list[Ranger]]
    seeds: list[int]
    maps, seeds = parse_lines(lines)

    min_loc = float("inf")
    for seed in seeds:
        s2s: int = source_to_dest(seed, maps["seed-to-soil map"])
        s2f: int = source_to_dest(s2s, maps["soil-to-fertilizer map"])
        f2w: int = source_to_dest(s2f, maps["fertilizer-to-water map"])
        w2li: int = source_to_dest(f2w, maps["water-to-light map"])
        li2t: int = source_to_dest(w2li, maps["light-to-temperature map"])
        t2h: int = source_to_dest(li2t, maps["temperature-to-humidity map"])
        htlo: int = source_to_dest(t2h, maps["humidity-to-location map"])

        min_loc = min(min_loc, htlo)
    print(min_loc)


def main():
    ipt: Path = Path("../input.txt")
    with (ipt.open(mode="r") as input_fi):
        lines: list[str] = input_fi.readlines()

    solution(lines)


if __name__ == "__main__":
    main()
