import abc
from collections import defaultdict, deque
from typing import cast

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=20)


class Term(abc.ABC):
    pass


class PathTerm(Term):
    def __init__(self, definition):
        self.definition = definition

    def __repr__(self):
        return self.definition


class LBracketTerm(Term):
    def __repr__(self):
        return '('


class RBracketTerm(Term):
    def __repr__(self):
        return ')'


class AlternativeTerm(Term):
    def __repr__(self):
        return '|'


class Node(abc.ABC):
    pass


class MainPath(Node):
    def __init__(self):
        self.parts = []

    def add_part(self, node: Node):
        self.parts.append(node)

    def __repr__(self):
        return ''.join([p.__repr__() for p in self.parts])


class BranchPath(Node):
    def __init__(self, options):
        self.options = options
        self.hasEmptyOption = None

    def add_part(self, node: Node):
        self.options.append(node)

    def __repr__(self):
        result = '('
        for idx, option in enumerate(self.options):
            result += option.__repr__()
            if idx != len(self.options) - 1:
                result += '|'
        result += ')'
        return result


class PathPart(Node):
    def __init__(self, definition):
        self.definition = definition

    def isEmpty(self):
        return len(self.definition) == 0

    def __repr__(self):
        return f'{self.definition}'


def split_to_terms(input_data):
    terms = []
    i = 1
    last_path_term = None
    while i < len(input_data) - 1:
        char = input_data[i]
        if char == '(':
            terms.append(LBracketTerm())
        elif char == ')':
            if last_path_term is None:
                terms.append(PathTerm(""))
            terms.append(RBracketTerm())
        elif char == '|':
            terms.append(AlternativeTerm())
            last_path_term = None
        else:
            definition = ''
            while i + 1 < len(input_data) and input_data[i + 1] in ['N', 'S', 'W', 'E']:
                definition += input_data[i]
                i += 1
            definition += input_data[i]
            term = PathTerm(definition)
            terms.append(term)
            last_path_term = term
        i += 1
    return terms


def split_to_subpaths(terms):
    groups = []
    last_idx = 0
    for idx, node in enumerate(terms):
        if type(node) is AlternativeTerm:
            groups.append(terms[last_idx: idx])
            last_idx = idx + 1
    groups.append(terms[last_idx:len(terms)])
    paths = []
    for group in groups:
        if len(group) == 1:
            paths.append(group[0])
        else:
            path = MainPath()
            for subpath in group:
                path.add_part(subpath)
            paths.append(path)
    return BranchPath(paths)


def build_branches_paths(terms):
    stack = deque()
    i = 0
    while i < len(terms):
        term = terms[i]
        if type(term) is PathTerm:
            stack.append(PathPart(term.definition))
        elif type(term) is LBracketTerm:
            stack.append(term)
        elif type(term) is AlternativeTerm:
            stack.append(term)
        elif type(term) is RBracketTerm:
            subpath = deque()
            while len(stack) > 0 and type(stack[-1]) is not LBracketTerm:
                term = stack.pop()
                subpath.appendleft(term)
            stack.pop()
            branch_path = split_to_subpaths(list(subpath))
            stack.append(branch_path)
        i += 1
    result = MainPath()
    while len(stack) > 0:
        part = stack.popleft()
        result.add_part(part)
    return result


def parse(input_data):
    terms = split_to_terms(input_data)
    path = build_branches_paths(terms)
    return path


DIRECTIONS = {
    'N': (-1, 0),
    'S': (1, 0),
    'W': (0, -1),
    'E': (0, 1),
}


def print_board(board):
    min_x = min(map(lambda x: x[1], board.keys()))
    max_x = max(map(lambda x: x[1], board.keys()))
    max_y = max(map(lambda x: x[0], board.keys()))
    min_y = min(map(lambda x: x[0], board.keys()))
    printable = [['#' for _ in range((max_x - min_x + 1) * 2 + 1)] for _ in range((max_y - min_y + 1) * 2 + 1)]
    for (y, x), doors in board.items():
        v_y = (y - min_y) * 2 + 1
        v_x = (x - min_x) * 2 + 1
        if y == 0 and x == 0:
            char = 'X'
        else:
            char = '.'
        printable[v_y][v_x] = char
        for dy, dx in doors:
            y_diff = y - dy
            x_diff = x - dx
            dy = v_y - y_diff
            dx = v_x - x_diff
            if y_diff == 0:
                printable[dy][dx] = "|"
            else:
                printable[dy][dx] = "-"

    print('\n'.join([''.join(row) for row in printable]))


def furthest_room(board):
    queue = deque([(0, 0)])
    dist = defaultdict(lambda: float('inf'))
    dist[(0, 0)] = 0
    visited = set()
    while len(queue) > 0:
        room = queue.popleft()
        if room in visited:
            continue
        for neighbour in board[room]:
            if dist[neighbour] > dist[room] + 1:
                dist[neighbour] = dist[room] + 1
                queue.append(neighbour)
    return max(dist.values())


def part1(input_data, debug=False):
    full_path = parse(input_data)
    board = defaultdict(set)
    board[(0, 0)] = set()

    def walk_node(part: PathPart, y, x):
        for direction in part.definition:
            dy, dx = DIRECTIONS[direction]
            new_y, new_x = y + dy, x + dx
            if debug: print(f'walk {y} {x} to {new_y} {new_x}')
            board[(y, x)].add((new_y, new_x))
            board[(new_y, new_x)].add((y, x))
            y, x = new_y, new_x
        return y, x

    def dfs(path: Node, y, x):
        if debug: print(f"{path} {y} {x}")
        if debug: print_board(board)
        if type(path) is PathPart:
            return walk_node(cast(PathPart, path), y, x)
        elif type(path) is MainPath:
            path = cast(MainPath, path)
            for part in path.parts:
                y, x = dfs(part, y, x)
        elif type(path) is BranchPath:
            path = cast(BranchPath, path)
            for node in path.options:
                dfs(node, y, x)
        return y, x

    dfs(full_path, 0, 0)

    return furthest_room(board)


def part2(input_data):
    data = parse(input_data)
    return -1


def main():
    assert 3 == part1("^WNE$")
    assert 2 == part1("^N(E|W)N$")
    #
    assert 10 == part1("^ENWWW(NEEE|SSE(EE|N))$")
    #
    assert 18 == part1("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$")
    assert 23 == part1("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")
    assert 31 == part1("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$")

    print("part1 examples OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    # assert 0 == part2(puzzle.examples[0].input_data)
    # print("part2 example OK")
    #
    # puzzle.answer_b = part2(puzzle.input_data)
    # print("part2 OK")


if __name__ == '__main__':
    main()

# ENWWW(NEEE|SSE(EE|N))
# ENWWW      |
# |          |
# NEEE      SSE
#          | |
#         EE N
