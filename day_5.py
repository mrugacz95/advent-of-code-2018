from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=5)


def are_different_polarity(a: str, b: str):
    return a.isupper() != b.isupper() and a.lower() == b.lower()


def shorten(polymer):
    idx = 1
    from_beginning = True
    while True:
        if are_different_polarity(polymer[idx], polymer[idx - 1]):
            polymer = polymer[:idx - 1] + polymer[idx + 1:]
            idx -= 2
            from_beginning = False
        else:
            if idx < len(polymer) - 1:
                idx += 1
            else:
                if from_beginning:
                    break
                else:
                    from_beginning = True
                    idx = 1
    print('done')
    return polymer


def part_1():
    data = puzzle.input_data
    polymer = shorten(data)
    puzzle.answer_a = len(polymer)


def part_2():
    data = puzzle.input_data
    unit_types = ['a', 'b', 'c', 'd']
    ans = min([len(shorten(data.replace(c, '').replace(c.upper(), ''))) for c in unit_types])
    puzzle.answer_b = ans


if __name__ == '__main__':
    # part_1()
    part_2()
