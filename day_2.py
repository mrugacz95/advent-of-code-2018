from collections import Counter
from typing import List

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=2)


def has_same_letters(number: int, box_id: str):
    counter = Counter(box_id)
    repeated = list(filter(lambda x: x[1] == number, counter.items()))
    return len(repeated) > 0


def choose_ids(box_ids: List[str]):
    rv = {2: [], 3: []}
    for id in box_ids:
        if has_same_letters(2, id):
            rv[2].append(id)
        if has_same_letters(3, id):
            rv[3].append(id)
    return rv


def part1():
    input = puzzle.input_data.split()
    box_ids = choose_ids(input)
    puzzle.answer_a = len(box_ids[3]) * len(box_ids[2])


def diff_on_one_pos(a, b):
    if len(a) != len(b):
        return False
    diff_count = 0
    diff_idx = None
    for idx, (c1, c2) in enumerate(zip(a, b)):
        if c1 != c2:
            if diff_count == 0:
                diff_count += 1
                diff_idx = idx
            else:
                return False, None
    return True, diff_idx


def part2():
    box_ids = puzzle.input_data.split()
    for idx1, id1 in enumerate(box_ids):
        for id2 in box_ids[idx1 + 1:]:
            diff, pos = diff_on_one_pos(id1, id2)
            if diff:
                puzzle.answer_b = str(id1[:pos] + id1[pos + 1:])
                return


if __name__ == '__main__':
    part1()
    part2()
