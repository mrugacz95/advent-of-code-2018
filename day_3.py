import re

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=3)


class Rect:
    PATTERN = r'#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)'

    def __init__(self, id, x, y, w, h):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @staticmethod
    def from_claim(claim):
        rectangle = re.match(Rect.PATTERN, claim)
        id = int(rectangle.group("id"))
        x = int(rectangle.group("x"))
        y = int(rectangle.group("y"))
        w = int(rectangle.group("w"))
        h = int(rectangle.group("h"))
        return Rect(id, x, y, w, h)

    def collide(self, other):
        return (self.x < other.x + other.w and
                self.x + self.w > other.x and
                self.y < other.y + other.h and
                self.y + self.h > other.y)

    def intersection(self, other):
        if self.collide(other):
            x = max(self.x, other.x)
            y = max(self.y, other.y)
            w = min(self.x + self.w, other.x + other.w) - x
            h = min(self.y + self.h, other.y + other.h) - y
            return Rect(None, x, y, w, h)

    def to_pieces(self):
        pieces = set()
        for x in range(self.x, self.x + self.w):
            for y in range(self.y, self.y + self.h):
                pieces.add((y, x))
        return pieces

    def area(self):
        return self.w * self.h

    def __repr__(self):
        return f'Rect#{self.id}<{self.x}, {self.y}, {self.w}, {self.y}>'


rectangles = list(map(Rect.from_claim, puzzle.input_data.split("\n")))


def part1():
    pieces = set()
    for idx, r1 in enumerate(rectangles):
        for r2 in rectangles[idx + 1:]:
            intersection = r1.intersection(r2)
            if intersection is not None:
                pieces.update(intersection.to_pieces())
    puzzle.answer_a = len(pieces)


def part2():
    for r1 in rectangles:
        for r2 in rectangles:
            if r1.id != r2.id and r1.collide(r2):
                break
        else:
            puzzle.answer_b = r1.id
            break


if __name__ == '__main__':
    part1()
    part2()
