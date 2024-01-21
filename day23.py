import re

from aocd.models import Puzzle
from z3 import Real, Solver, Optimize, If

puzzle = Puzzle(year=2018, day=23)


def parse(input_data):
    parsed = []
    for line in input_data.split("\n"):
        match = re.findall(r"-?\d+", line)
        parsed.append(tuple(map(int, match)))
    return parsed


def distance(p1, p2):
    return sum(map(lambda p: abs(p[0] - p[1]), zip(p1, p2)))


def in_sphere(center, radius, point):
    dist = distance(center, point)
    return dist >= radius


def argmax(array):
    return array.index(max(array))


def part1(input_data):
    nanobots = parse(input_data)
    strongest_idx = argmax(list(map(lambda r: r[3], nanobots)))
    in_range = 0
    sx, sy, sz, r = nanobots[strongest_idx]
    for (nx, ny, nz, _) in nanobots:
        if distance((sx, sy, sz), (nx, ny, nz)) <= r:
            in_range += 1
    return in_range


def part2(input_data):
    opt = Optimize()
    nanobots = parse(input_data)
    x = Real('x')
    y = Real('y')
    z = Real('z')

    def sabs(x):
        return If(x >= 0, x, -x)

    for (cx, cy, cz, cr) in nanobots:
        opt.add_soft(sabs(cx - x) + sabs(cy - y) + sabs(cz - z) <= cr)
    opt.minimize(sabs(x) + sabs(y) + sabs(z))  # distance to 0,0,0
    opt.check()
    model = opt.model()
    x, y, z = model[x].as_long(), model[y].as_long(), model[z].as_long(),
    return abs(x) + abs(y) + abs(z)


def main():
    assert 7 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    example = ("pos=<10,12,12>, r=2\n"
               "pos=<12,14,12>, r=2\n"
               "pos=<16,12,12>, r=4\n"
               "pos=<14,14,14>, r=6\n"
               "pos=<50,50,50>, r=200\n"
               "pos=<10,10,10>, r=5")
    assert 36 == part2(example)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
