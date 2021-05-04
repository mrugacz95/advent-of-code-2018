from functools import reduce
from operator import add

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=12)
raw = puzzle.input_data.split('\n')

EMPTY = '.'
FULL = '#'


def part_1(init, rules):
    generations = 20
    rule_len = 5
    full_pots = set(map(lambda pot: pot[0], filter(lambda pot: pot[1] == FULL, enumerate(init))))
    min_plant_id = min(full_pots)
    max_plant_id = max(full_pots)
    for _ in range(generations):
        new_pots = set()
        for start in range(min_plant_id - rule_len + 1, max_plant_id + rule_len):
            state = ''
            for pos in range(rule_len):
                if start + pos in full_pots:
                    state += FULL
                else:
                    state += EMPTY
            if state in rules and rules[state] == FULL:
                center = start + 2
                min_plant_id = min(center, min_plant_id)
                max_plant_id = max(center, min_plant_id)
                new_pots.add(center)
        full_pots = new_pots
    return reduce(add, full_pots, 0)


def solve():
    assert part_1('#..#.#..##......###...###',
                  {'...##': '#', '..#..': '#', '.#...': '#',
                   '.#.#.': '#', '.#.##': '#', '.##..': '#',
                   '.####': '#', '#.#.#': '#', '#.###': '#',
                   '##.#.': '#', '##.##': '#', '###..': '#',
                   '###.#': '#', '####.': '#'}) == 325

    initial = raw[0].replace('initial state: ', '')
    rules = {lhs: rhs for lhs, rhs in map(lambda row: row.split(' => '), raw[2:])}

    ans = part_1(initial, rules)
    puzzle.answer_a = ans


if __name__ == '__main__':
    solve()
