import itertools
import string
from collections import deque, defaultdict
from functools import cmp_to_key
from math import ceil, log

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=6)

raw = puzzle.input_data


class Point:
    def __init__(self, y, x, name=None):
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return f"{self.name}({self.y}, {self.x})"

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - other.x * self.y

    def __sub__(self, other):
        return Point(self.y - other.y, self.x - other.x, None)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.y - other.y, self.x - other.x, None)

    def __abs__(self):
        return Point(abs(self.y), abs(self.x), None)

    def manth_dist(self, other):
        vec = self - other
        vec = abs(vec)
        return vec.y + vec.x

    def __hash__(self):
        return (self.y, self.x).__hash__()

    def rename(self, name):
        self.name = name
        return self


def parse_data(data):
    data = data.split("\n")
    points = []
    names_len = ceil(log(len(data), len(string.ascii_uppercase)))
    names = itertools.product(string.ascii_uppercase, repeat=names_len)
    for point, name in zip(data, names):
        y, x = map(int, point.split(", "))
        name = ''.join(name)
        points.append(Point(y, x, name))
    return points


data = parse_data(raw)


def turn(p1: Point, p2: Point, p3: Point):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)


def solve():
    # Graham scan is probably not needed
    points = sorted(data, key=lambda p: (p.y, p.x))
    first = points[0]
    points = list(map(lambda p: (p - first).rename(p.name), points))
    first = points[0]
    points = sorted(points, key=cmp_to_key(lambda a, b: a.cross(b)))
    stack = deque()
    for point in points:
        while len(stack) > 1 and turn(stack[-2], stack[-1], point) > 0:
            stack.pop()
        stack.append(point)
    inside = list(filter(lambda p: p not in stack, points))

    def closest_to(cell: Point):
        distances = defaultdict(list)
        for point in points:
            dist = cell.manth_dist(point)
            distances[dist].append(point)
        return distances

    min_x = min(map(lambda p: p.x, points))
    max_x = max(map(lambda p: p.x, points))
    min_y = min(map(lambda p: p.y, points))
    max_y = max(map(lambda p: p.y, points))

    def get_min_key(dictionary):
        min_key = min(dictionary.keys())
        if len(dictionary[min_key]) == 1:
            min_val = dictionary[min_key][0]
        else:
            min_val = None
        return min_val

    def flood_fill(beginning: Point):
        visited = set()
        q = deque()
        q.append(beginning)
        while len(q) != 0:
            point = q.pop()
            closest = closest_to(point)
            closest = get_min_key(closest)
            if point in visited or closest != beginning:
                continue
            visited.add(point)
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for y, x in directions:
                new_point = point + Point(y, x)
                if new_point.x < min_x or new_point.x > max_x:
                    continue
                if new_point.y < min_y or new_point.y > max_y:
                    continue
                if new_point not in visited:
                    q.append(new_point)
        return len(visited)

    ans = 0
    for point in inside:
        area = flood_fill(point)
        if area > ans:
            ans = area
    puzzle.answer_a = ans

    region_size = 0
    for y in range(min_y, max_y + 1):
        print(y)
        found_row = False
        for x in range(min_x, max_x + 1):
            closest = closest_to(Point(y, x))
            sum_dist = 0
            for dist, distance_points in closest.items():
                sum_dist += dist * len(distance_points)
            if sum_dist < 10000:
                region_size += 1
                found_row = True
            elif found_row:
                break
    puzzle.answer_b = region_size


if __name__ == '__main__':
    solve()
