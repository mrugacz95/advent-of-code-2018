import enum
import heapq
import re
from collections import deque, defaultdict
from functools import cache

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=22)


def parse(input_data):
    match = re.search(r'depth: (?P<depth>(\d+))\ntarget: (?P<x>(\d+)),(?P<y>(\d+))', input_data)
    return int(match.group('depth')), int(match.group('y')), int(match.group('x'))


@cache
def get_geologic_index(y, x, target_x, target_y, depth):
    if y == 0 and x == 0:
        return 0
    if y == target_y and x == target_x:
        return 0
    if y == 0 and x == 0:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return get_erosion_lvl(y - 1, x, target_x, target_y, depth) * get_erosion_lvl(y, x - 1, target_x, target_y, depth)


@cache
def get_erosion_lvl(y, x, target_x, target_y, depth):
    return (get_geologic_index(y, x, target_x, target_y, depth) + depth) % 20183


@cache
def get_type(y, x, target_x, target_y, depth):
    return get_erosion_lvl(y, x, target_x, target_y, depth) % 3


def part1(input_data):
    depth, target_x, target_y = parse(input_data)
    risk = 0
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            risk += get_type(y, x, target_x, target_y, depth)
    return risk


class Tool(enum.Enum):
    TORCH = 0
    NEITHER = 1
    CLIMBING_GEAR = 2

    def __lt__(self, other):
        return self.value < other.value


def get_possible_tools(type):
    if type == 0:  # rocky
        return [Tool.TORCH, Tool.CLIMBING_GEAR]
    if type == 1:  # wet
        return [Tool.CLIMBING_GEAR, Tool.NEITHER]
    if type == 2:  # narrow
        return [Tool.TORCH, Tool.NEITHER]


def is_tool_useful(tool, y, x, target_x, target_y, depth):
    type = get_type(y, x, target_x, target_y, depth)
    return tool in get_possible_tools(type)


TOOL_CHANGE_TIME = 7
MOVEMENT_TIME = 1


def print_board(target, depth, pos):
    ty, tx = target
    py, px = pos
    for y in range(ty + 6):
        for x in range(tx + 6):
            if (y, x) == (py, px):
                char = 'X'
            elif (y, x) == (0, 0):
                char = 'M'
            elif (y, x) == (ty, tx):
                char = 'T'
            else:
                type = get_type(y, x, ty, tx, depth)
                char = {
                    0: '.',
                    1: '=',
                    2: '|'
                }.get(type)
            print(char, end='')
        print()
    print()


def dfs(target, depth, debug):
    ty, tx = target
    sy, sx = 0, 0
    heap = [(0, Tool.TORCH, sy, sx)]  # stat at t0 in 0,0 with torch
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    cost = defaultdict(lambda: float('inf'))
    cost[(0, 0, Tool.TORCH)] = 0  # time, y, x, tool 0-torch
    prev = {(0, 0, Tool.TORCH): (-1, -1, None)}
    visited = set()
    while len(heap) > 0:
        time, tool, y, x = heapq.heappop(heap)
        if (y, x, tool) in visited:
            continue
        cost[y, x] = time
        visited.add((y, x, tool))
        if (y, x) == target and tool == Tool.TORCH:
            print(time)
            break

        def add_node_to_queue(new_y, new_x, new_tool, new_cost):
            heapq.heappush(heap, (new_time, new_tool, new_y, new_x))
            if cost[(new_y, new_x, new_tool)] > new_cost:
                cost[(new_y, new_x, new_tool)] = new_cost
                prev[(new_y, new_x, new_tool)] = (y, x, tool)

        # check neighbours
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny and 0 <= nx:
                if is_tool_useful(tool, ny, nx, ty, tx, depth):
                    new_time = time + MOVEMENT_TIME
                    add_node_to_queue(ny, nx, tool, new_time)
        # check tool change
        region_type = get_type(y, x, tx, ty, depth)
        for next_tool in get_possible_tools(region_type):
            if next_tool != tool:
                new_time = time + TOOL_CHANGE_TIME
                add_node_to_queue(y, x, next_tool, new_time)
    if debug:
        cy, cx, ct = (ty, tx, Tool.TORCH)
        path = deque()
        path.append((cy, cx, ct))
        while True:
            cy, cx, ct = prev[(cy, cx, ct)]
            path.appendleft((cy, cx, ct))
            if prev[(cy, cx, ct)][2] is None:
                break
        print("Initially:")
        print_board(target, depth, (0, 0))
        for i in range(1, len(path)):
            (py, px, pt) = path[i - 1]
            (cy, cx, ct) = path[i]
            if pt == ct:
                if py + 1 == cy:
                    print(f"Down:")
                elif py - 1 == cy:
                    print(f"Up:")
                elif px + 1 == cx:
                    print(f"Right:")
                elif px - 1 == cx:
                    print(f"Left:")
            else:
                print(f"Switch from using {pt} to {ct}")
            print_board(target, depth, (cy, cx))
    return cost[(ty, tx)]


def part2(input_data, debug=False):
    depth, target_y, target_x = parse(input_data)
    time = dfs((target_y, target_x), depth, debug)
    return time


def main():
    assert 114 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert 45 == part2(puzzle.examples[0].input_data, True)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
