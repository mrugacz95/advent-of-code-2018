from collections import Counter
from functools import reduce

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=18)


def parse(input_data):
    return [list(line) for line in input_data.split("\n")]


NEIGHBOURS = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1),
    (1, -1),
    (1, 1),
    (-1, 1),
    (-1, -1),
]


def get_neighbours(board, pos):
    neighbours = []
    for dy, dx in NEIGHBOURS:
        ny, nx = pos[0] + dy, pos[1] + dx
        if 0 <= ny < len(board) and 0 <= nx < len(board[0]):
            neighbours.append(board[ny][nx])
    return neighbours


def game_of_life(board):
    new_board = [[None for cell in row] for row in board]
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            new_char = cell
            counter = Counter(get_neighbours(board, (y, x)))
            if cell == ".":
                if counter["|"] >= 3:
                    new_char = "|"
            elif cell == "|":
                if counter["#"] >= 3:
                    new_char = "#"
            elif cell == "#":
                if counter["#"] >= 1 and counter["|"] >= 1:
                    new_char = "#"
                else:
                    new_char = "."
            new_board[y][x] = new_char
    return new_board


def print_board(board):
    for row in board:
        print("".join(row))
    print()


def part1(input_data):
    board = parse(input_data)
    for _ in range(10):
        board = game_of_life(board)
        print_board(board)
    counter = Counter()
    for row in board:
        counter.update(row)
    return counter["|"] * counter["#"]


def hash_board(board):
    return hash(tuple(tuple(row) for row in board))


def find_cycle(array):
    for l in range(4, len(array) // 2):
        a1 = array[-l:]
        a2 = array[-2 * l: -l]
        if a1 == a2:
            return l
    return None


def calc_resources(board):
    counter = Counter()
    for row in board:
        counter.update(row)
    return counter["|"] * counter["#"]


def part2(input_data):
    board = parse(input_data)
    hashes = list()
    hashes.append(hash_board(board))
    resources_values = []
    cycle_length = None
    while True:
        board = game_of_life(board)
        hashes.append(hash_board(board))
        resources_values.append(calc_resources(board))
        cycle_length = find_cycle(hashes)
        if cycle_length is not None:
            break
    cycle_start = len(hashes) - cycle_length
    needed_cycles = 1_000_000_000
    reminding_cycles = needed_cycles - cycle_start - 1
    last_cycle = cycle_start + reminding_cycles % cycle_length
    return resources_values[last_cycle]


def main():
    assert 1147 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert find_cycle([4, 5, 6, 7, 12, 13, 14, 15, 16, 12, 13, 14, 15, 16]) == 5
    assert find_cycle([4, 5, 6, 7, 12, 13, 14, 10, 16, 12, 13, 14, 15, 16]) is None
    print("part2 tests OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
