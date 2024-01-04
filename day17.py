from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=17)


def parse(input_data):
    ranges = []
    for line in input_data.split("\n"):
        ranges_in_line = line.split(", ")

        def parse_range(text):
            dim = text[0]
            text = text[2:]
            if '..' in text:
                start, end = text.split('..')
                return dim, int(start), int(end)
            else:
                return dim, int(text), int(text)

        line_y_x = {}
        for single_range in ranges_in_line:
            dim, start, end = parse_range(single_range)
            line_y_x[dim] = (start, end + 1)
        ranges.append((line_y_x['y'], line_y_x['x']))
    return ranges


def map_to_ground(ranges):
    ground = {}
    for (y_start, y_end), (x_start, x_end) in ranges:
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                ground[(y, x)] = "#"
    return ground


def print_ground(ground):
    min_x = min(map(lambda pos: pos[1], ground.keys())) - 1
    max_x = max(map(lambda pos: pos[1], ground.keys()))
    min_y = min(map(lambda pos: pos[0], ground.keys())) - 1
    max_y = max(map(lambda pos: pos[0], ground.keys()))
    board = [['.' for x in range(min_x - 1, max_x + 1)] for y in range(min_y - 1, max_y + 1)]
    for (y, x), v in ground.items():
        board[y - min_y + 1][x - min_x + 1] = v
    for row in board:
        for cell in row:
            print(cell, end='')
        print()
    print()


def flow_water(ground, max_y):
    def get(y, x):
        if (y, x) in ground:
            return ground[(y, x)]
        else:
            return None

    y, x = None, None
    for (node_y, node_x), v in ground.items():
        if v == "|" and node_y + 1 <= max_y:
            if (node_y + 1, node_x) not in ground:  # hanging water
                y, x = node_y, node_x
                break
            if (get(node_y + 1, node_x) is not None and get(node_y + 1, node_x) == '~' and  # is above water surface
                    (get(node_y, node_x + 1) is None or get(node_y, node_x - 1) is None)):  # didnt splashed yet
                y, x = node_y, node_x
                break
            if (get(node_y + 1, node_x) is not None and get(node_y + 1, node_x) == '~' and  # is above water surface
                    get(node_y, node_x + 1) == '#' and get(node_y, node_x - 1) == '#'):  # in narrow flask
                y, x = node_y, node_x
                break
    if y is None:
        return True
    # flow down
    while get(y + 1, x) not in ['#', '~'] and y + 1 <= max_y:
        ground[(y, x)] = '|'
        y += 1
    # splash horizontally
    splash = [(y, x)]
    will_fall = False
    right_x = x
    while get(y + 1, right_x) in ["#", "~"] and (get(y, right_x + 1) != '#'):
        right_x += 1
        splash.append((y, right_x))
    if get(y + 1, right_x) in ["|", None]:
        will_fall = True
    left_x = x
    while get(y + 1, left_x) in ["#", "~"] and (get(y, left_x - 1) != '#'):
        left_x -= 1
        splash.append((y, left_x))
    if get(y + 1, left_x) in ["|", None]:
        will_fall = True
    if will_fall:
        char = "|"
    else:
        char = "~"
    for coord in splash:
        ground[coord] = char
    return False


def part1(input_data):
    ranges = parse(input_data)
    ground = map_to_ground(ranges)
    ground[(0, 500)] = '|'
    print_ground(ground)
    min_y = min(map(lambda item: item[0][0], filter(lambda item: item[1] == '#', ground.items())))
    max_y = max(map(lambda item: item[0][0], filter(lambda item: item[1] == '#', ground.items())))
    while True:
        finished = flow_water(ground, max_y)
        if finished:
            break
    print_ground(ground)
    counter = 0
    for (y, x), v in ground.items():
        if v in ["|", "~"] and min_y <= y <= max_y:
            counter += 1
    return counter


def part2(input_data):
    ranges = parse(input_data)
    ground = map_to_ground(ranges)
    ground[(0, 500)] = '|'
    min_y = min(map(lambda item: item[0][0], filter(lambda item: item[1] == '#', ground.items())))
    max_y = max(map(lambda item: item[0][0], filter(lambda item: item[1] == '#', ground.items())))
    while True:
        finished = flow_water(ground, max_y)
        if finished:
            break
    counter = 0
    for (y, x), v in ground.items():
        if v == "~" and min_y <= y <= max_y:
            counter += 1
    return counter


def main():
    assert 57 == part1(puzzle.examples[0].input_data)

    example_1 = ("x=499, y=2..7\n"
                 "x=501, y=2..7\n"
                 "y=7, x=499..501\n"
                 "x=506, y=1..2")

    assert 22 == part1(example_1)

    example_2 = ("x=498, y=2..7\n"
                 "x=506, y=2..7\n"
                 "y=7, x=498..506\n"
                 "x=503, y=4..6\n"
                 "x=512, y=1..2")

    assert 55 == part1(example_2)

    example_3 = ("x=499, y=2..4\n"
                 "x=501, y=2..4\n"
                 "y=4, x=499..501\n"
                 "x=497, y=7..10\n"
                 "x=506, y=7..10\n"
                 "y=10, x=497..506\n"
                 "x=513, y=1..2")
    assert 59 == part1(example_3)

    example_4 = ("x=499, y=2..4\n"
                 "x=505, y=2..4\n"
                 "y=4, x=499..505\n"
                 "x=497, y=6..8\n"
                 "x=503, y=7..8\n"
                 "y=8, x=497..503\n"
                 "x=507, y=13..15\n"
                 "x=501, y=13..15\n"
                 "y=16, x=501..507\n"
                 "x=513, y=1..2")
    assert 82 == part1(example_4)

    print("part1 example OK")
    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert 29 == part2(puzzle.examples[0].input_data)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
