import re

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=25)


def parse(input_data):
    points = []
    for line in input_data.split("\n"):
        coords = tuple(map(int, re.findall(r"(-?\d+)", line)))
        points.append(coords)
    return points


def manhattan_distance(point1, point2):
    return sum(map(lambda p: abs(p[0] - p[1]), zip(point1, point2)))


def distance(point, constellation):
    dist = float('inf')
    for p in constellation:
        dist = min(dist, manhattan_distance(p, point))
    return dist


def part1(input_data):
    points = parse(input_data)
    connections = [[False for _ in range(len(points))] for _ in range(len(points))]
    for i, pi in enumerate(points):
        for j, pj in enumerate(points):
            if i < j:
                connected = manhattan_distance(pi, pj) <= 3
                connections[i][j] = connected
                connections[j][i] = connected
    visited = [False for _ in range(len(points))]

    def dfs(start):
        if visited[start]:
            return False
        visited[start] = True
        for neighbor, conn in enumerate(connections[start]):
            if conn:
                dfs(neighbor)
        return True

    constellations = 0
    for i in range(len(points)):
        if dfs(i):
            constellations += 1
    return constellations


def part2(input_data):
    data = parse(input_data)
    return -1


def main():
    for i, example in enumerate(puzzle.examples):
        assert int(example.answer_a) == part1(example.input_data), f"Example {i} failed"
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")


if __name__ == '__main__':
    main()
