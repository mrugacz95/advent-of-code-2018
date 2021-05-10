from functools import reduce
from operator import add

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=12)
raw = puzzle.input_data.split('\n')

EMPTY = '.'
FULL = '#'


def step(full_pots, rules, generations):
    rule_len = len(next(iter(rules.keys())))
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
    return full_pots


def part_1(initial, rules, generations=20):
    full_pots = set(map(lambda pot: pot[0], filter(lambda pot: pot[1] == FULL, enumerate(initial))))
    full_pots = step(full_pots, rules, generations)
    return reduce(add, full_pots, 0)


def part_2(initial, rules, generations):
    if generations < 200:
        return part_1(initial, rules, generations)
    full_pots = set(map(lambda pot: pot[0], filter(lambda pot: pot[1] == FULL, enumerate(initial))))
    plants_score = []
    required_repeat_length = 50
    while True:
        plants_score.append(reduce(add, full_pots, 0))
        full_pots = step(full_pots, rules, 1)
        if len(plants_score) < required_repeat_length:
            continue
        last_counts = plants_score[-required_repeat_length:]
        last_diffs = []
        for i in range(1, len(last_counts)):
            last_diffs.append(last_counts[i] - last_counts[i - 1])
        unique_diffs = set(last_diffs)
        if len(unique_diffs) > 1:
            continue
        break
    generations_done = len(plants_score)
    diff = plants_score[-1] - plants_score[-2]
    generations_left = generations - generations_done + 1
    return plants_score[-1] + generations_left * diff


def solve():
    test_init = '#..#.#..##......###...###'
    test_rules = {'...##': '#', '..#..': '#', '.#...': '#',
                  '.#.#.': '#', '.#.##': '#', '.##..': '#',
                  '.####': '#', '#.#.#': '#', '#.###': '#',
                  '##.#.': '#', '##.##': '#', '###..': '#',
                  '###.#': '#', '####.': '#'}
    assert part_1(test_init, test_rules) == 325

    assert part_1(test_init, test_rules, 350) == part_2(test_init, test_rules, 350)

    initial = raw[0].replace('initial state: ', '')

    rules = {lhs: rhs for lhs, rhs in map(lambda row: row.split(' => '), raw[2:])}

    ans = part_1(initial, rules)
    puzzle.answer_a = ans

    ans = part_2(initial, rules, 50000000000)
    puzzle.answer_b = ans


if __name__ == '__main__':
    solve()
