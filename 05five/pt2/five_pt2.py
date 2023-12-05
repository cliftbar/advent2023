from dataclasses import dataclass
from pathlib import Path

maps_flat: dict[str, list[tuple[int, int, int]]]


@dataclass
class SingleRange:
    start: int
    stop: int


@dataclass
class MapRanger:
    source: int
    step: int
    dest_offset: int

    def in_range(self, source) -> bool:
        return self.source <= source < self.source + self.step

    def intersects(self, seed: range):
        this = range(self.source, self.source + self.step - 1)

        # seed is totally enclosed (inclusive)
        # seed  :     |34|
        # source: |12  34 5| + 10
        # done: [13,14]
        # cont: []
        if this.start <= seed.start and seed.stop <= this.stop:
            return [range(seed.start + self.dest_offset, seed.stop + self.dest_offset)], []

        # this totally enclosed (exclusive)
        # source:     |34|
        # seed  : |12  34 5|
        # done: [13,14]
        # cont: [1,2][5,5]
        if seed.start < this.start and this.stop < seed.stop:
            return ([range(this.start + self.dest_offset, this.stop + self.dest_offset)],
                    [range(seed.start, this.start - 1), range(this.stop + 1, seed.stop)])

        # seed totally below (exclusive)
        # source:      |45|
        # seed  : |123|
        # done: []
        # cont: [1,3]
        if seed.stop < this.start:
            return [], [seed]
        # seed totally above (exclusive)
        # seed  :      |45|
        # source: |123|
        # done: []
        # cont: [4,5]
        if this.stop < seed.start:
            return [], [seed]

        # seed overlaps below
        # source:     |345| + 10
        # seed  : |12  34|
        # done: [13,14]
        # cont: [1,2]
        if seed.start < this.start and seed.stop <= this.stop:
            return ([range(this.start + self.dest_offset, seed.stop + self.dest_offset)],
                    [range(seed.start, this.start - 1)])

        # seed overlaps above
        # source: |012| + 10
        # seed  :  |12  34|
        # done: [11,12]
        # cont: [3,4]
        if this.start <= seed.start and this.stop < seed.stop:
            return ([range(seed.start + self.dest_offset, this.stop + self.dest_offset)],
                    [range(this.stop + 1, seed.stop)])

        raise Exception("AAAAAhhhhhhh")

    @staticmethod
    def from_line(line: str) -> "MapRanger":
        d, s, st = line.strip(".").split(" ")
        source = int(s)
        dest = int(d)
        step = int(st)
        dest_offset = dest - source
        return MapRanger(source, step, dest_offset)


def parse_lines(lines: list[str]) -> (dict[str, list[MapRanger]], list[int]):
    sections: list[str] = ".".join(lines).split(".\n")

    seeds: list[int] = list(map(int, sections[0].split(": ")[1].split(" ")))

    ret_map: dict[str, list[MapRanger]] = {}
    for sec in sections[1:]:
        sec_lines = sec.strip().strip(".").split("\n")
        map_type: str = sec_lines[0][:-1]

        range_list: list[MapRanger] = []
        for sl in sec_lines[1:]:
            r = MapRanger.from_line(sl.strip("."))
            range_list.append(r)

        ret_map[map_type] = range_list

    return ret_map, seeds


def process_map_type(seed_ranges: list[range], mappings: list[MapRanger]) -> list[range]:
    ret_num: list[range] = []
    looping_ranges: list[range] = seed_ranges
    mr: MapRanger
    for mr in mappings:
        missed_ranges = []
        for sr in looping_ranges:
            hit, missed = mr.intersects(sr)
            ret_num += hit
            missed_ranges += missed
        looping_ranges = missed_ranges

    ret_num += looping_ranges
    return ret_num


def search_seed_pair(start_seed: int, end_seed_step: int, maps: dict[str, list[MapRanger]]) -> list[range]:
    seed_ranges: list[range] = [range(start_seed, start_seed + end_seed_step)]
    map_type: str
    _map: list[MapRanger]

    final_ranges: list[range] = seed_ranges
    next_ranges: list[range] = []
    for map_type, _map in maps.items():
        # print(map_type)
        final_ranges = process_map_type(final_ranges, _map)
        # print(final_ranges)

    # return locations
    return final_ranges


def solution(lines: list[str]):
    maps: dict[str, list[MapRanger]]

    seeds: list[int]
    maps, seeds = parse_lines(lines)

    location_ranges: list[range] = []
    for i in range(0, len(seeds), 2):
        location_ranges += search_seed_pair(seeds[i], seeds[i + 1] - 1, maps)
    print(min([lo.start for lo in location_ranges]))


def main():
    ipt: Path = Path("../input.txt")
    # ipt: Path = Path("../sample_input.txt")
    with (ipt.open(mode="r") as input_fi):
        lines: list[str] = input_fi.readlines()

    solution(lines)  # 31161857


if __name__ == "__main__":
    main()
