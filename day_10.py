import re

import pytesseract
from PIL import Image, ImageDraw
from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=10)
raw = puzzle.input_data


# raw = """position=< 9,  1> velocity=< 0,  2>
# position=< 7,  0> velocity=<-1,  0>
# position=< 3, -2> velocity=<-1,  1>
# position=< 6, 10> velocity=<-2, -1>
# position=< 2, -4> velocity=< 2,  2>
# position=<-6, 10> velocity=< 2, -2>
# position=< 1,  8> velocity=< 1, -1>
# position=< 1,  7> velocity=< 1,  0>
# position=<-3, 11> velocity=< 1, -2>
# position=< 7,  6> velocity=<-1, -1>
# position=<-2,  3> velocity=< 1,  0>
# position=<-4,  3> velocity=< 2,  0>
# position=<10, -3> velocity=<-1,  1>
# position=< 5, 11> velocity=< 1, -2>
# position=< 4,  7> velocity=< 0, -1>
# position=< 8, -2> velocity=< 0,  1>
# position=<15,  0> velocity=<-2,  0>
# position=< 1,  6> velocity=< 1,  0>
# position=< 8,  9> velocity=< 0, -1>
# position=< 3,  3> velocity=<-1,  1>
# position=< 0,  5> velocity=< 0, -1>
# position=<-2,  2> velocity=< 2,  0>
# position=< 5, -2> velocity=< 1,  2>
# position=< 1,  4> velocity=< 2,  1>
# position=<-2,  7> velocity=< 2, -2>
# position=< 3,  6> velocity=<-1, -1>
# position=< 5,  0> velocity=< 1,  0>
# position=<-6,  0> velocity=< 2,  0>
# position=< 5,  9> velocity=< 1, -2>
# position=<14,  7> velocity=<-2,  0>
# position=<-3,  6> velocity=< 2, -1>"""


class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def __repr__(self):
        return f'<P: x={self.x}, y={self.y}, vx={self.vx}, vy={self.vy}>'


def parse_points(data):
    pattern = r'position=< *(?P<x>-?\d+), *(?P<y>-?\d+)> velocity=< *(?P<vx>-?\d+), *(?P<vy>-?\d+)>'
    points = []
    for line in data.split("\n"):
        point = re.match(pattern, line)
        x = int(point.group('x'))
        y = int(point.group('y'))
        vx = int(point.group('vx'))
        vy = int(point.group('vy'))
        points.append(Point(x, y, vx, vy))
    return points


def print_points(points):
    white = 1
    black = 0
    margin = 10
    resize_x = 4
    resize_y = 5
    min_x = min([point.x for point in points]) - margin
    max_x = max([point.x for point in points]) + margin
    min_y = min([point.y for point in points]) - margin
    max_y = max([point.y for point in points]) + margin
    width = (max_x - min_x) * resize_x
    height = (max_y - min_y) * resize_y
    possible_size = 512 * 1024  # 512 Kb
    if width * height > possible_size:
        return None  # too big to draw
    img = Image.new('1', size=(width, height), color=white)
    draw = ImageDraw.Draw(img)
    for point in points:
        x = (point.x - min_x) * resize_x
        y = (max_y - point.y) * resize_y
        draw.rectangle((x, y, x + resize_x, y + resize_y), fill=black)
    return img


def solve():
    points = parse_points(raw)
    second = 0
    while True:
        img = print_points(points)
        if img is not None:
            text = pytesseract.image_to_string(img)
            text = text.strip()
            print(text)
            if text != '' and any([c.isupper() for c in text]):
                print(text)
                img.show()
                break
        [point.move() for point in points]
        second += 1
    puzzle.answer_b = second


if __name__ == '__main__':
    solve()
