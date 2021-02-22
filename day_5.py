from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=5)


def are_different_polarity(a: str, b: str):
    return a.isupper() != b.isupper() and a.lower() == b.lower()


def shorten(polymer):
    idx = 1
    while True:
        if are_different_polarity(polymer[idx], polymer[idx - 1]):
            polymer = polymer[:idx - 1] + polymer[idx + 1:]
            idx -= 1
        else:
            if idx < len(polymer) - 1:
                idx += 1
            else:
                break
    return polymer


def part_1():
    data = puzzle.input_data
    polymer = shorten(data)
    puzzle.answer_a = len(polymer)


def part_2():
    data = puzzle.input_data
    polimer = shorten(data)
    unit_types = set(polimer.lower())
    min_len = float('inf')
    for c in unit_types:
        short = shorten(polimer.replace(c, '').replace(c.upper(), ''))
        min_len = min(min_len, len(short))
    puzzle.answer_b = min_len


if __name__ == '__main__':
    part_1()
    part_2()
