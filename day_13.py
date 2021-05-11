from collections import defaultdict
from enum import Enum
from typing import Dict, Optional, Tuple

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=13)
left_turn = '∖'
raw = puzzle.input_data.replace('\\', left_turn)


def format(*args):
    return '\n'.join(args)


one_loop = format('/->-∖',
                  '|   |',
                  '|   |',
                  '|   |',
                  '∖---/')

three_loops = format('/->-∖        ',
                     '|   |  /----∖',
                     '| /-+--+-∖  |',
                     '| | |  | v  |',
                     '∖-+-/  ∖-+--/',
                     '  ∖------/   ')
crash = format('|',
               'v',
               '|',
               '|',
               '|',
               '^',
               '|', )

eight_shape = format('/--∖    ',
                     '|  |    ',
                     '|  |    ',
                     '∖--+---∖',
                     '   |   |',
                     '   v   |',
                     '   |   |',
                     '   ∖---/')

close_loop = format('/-∖        ',
                    '| | /-----∖',
                    '∖-+-+---∖ |',
                    '  | v   | |',
                    '  ∖-+---/ |',
                    '    ∖---∖ |',
                    '        | |',
                    '        ∖-/')

wreckfest = format('/>-<∖  ',
                   '|   |  ',
                   '| /<+-∖',
                   '| | | v',
                   '∖>+</ |',
                   '  |   ^',
                   '  ∖<->/')


class SimpleReprDefaultDict(defaultdict):
    def __repr__(self):
        return repr(dict(self))


class Direction(Enum):
    _ignore_ = ['_cart_to_direction', '_direction_to_cart']
    UP = 1
    DOWN = -1
    LEFT = -2
    RIGHT = 2
    STRAIGHT = 4

    def __lt__(self, other: 'Direction'):
        return self.value < other.value

    _cart_to_direction = {}
    _direction_to_cart = {}

    def apply(self, y, x):
        return {
            Direction.UP: (y - 1, x),
            Direction.DOWN: (y + 1, x),
            Direction.LEFT: (y, x - 1),
            Direction.RIGHT: (y, x + 1)
        }.get(self)

    @staticmethod
    def from_cart(cart):
        return Direction._cart_to_direction[cart]

    def to_cart(self):
        return self._direction_to_cart[self]

    def opposite(self):
        return Direction(-self.value)

    def __repr__(self):
        return {
            Direction.RIGHT: "RIGHT",
            Direction.LEFT: "LEFT",
            Direction.UP: "UP",
            Direction.DOWN: "DOWN",
            Direction.STRAIGHT: "STRAIGHT",
        }.get(self)

    @staticmethod
    def to_relative_direction(before: 'Direction', after: 'Direction'):
        if before.opposite() == after:
            return Direction.STRAIGHT
        return {
            # right
            (Direction.LEFT, Direction.DOWN): Direction.RIGHT,
            (Direction.DOWN, Direction.RIGHT): Direction.RIGHT,
            (Direction.RIGHT, Direction.UP): Direction.RIGHT,
            (Direction.UP, Direction.LEFT): Direction.RIGHT,
            # left
            (Direction.LEFT, Direction.UP): Direction.LEFT,
            (Direction.DOWN, Direction.LEFT): Direction.LEFT,
            (Direction.RIGHT, Direction.DOWN): Direction.LEFT,
            (Direction.UP, Direction.RIGHT): Direction.LEFT,
        }.get((before, after))

    @staticmethod
    def from_relative_direction(relative, absolute):
        if relative == Direction.STRAIGHT:
            return absolute
        if relative == Direction.LEFT:
            return {
                Direction.LEFT: Direction.DOWN,
                Direction.RIGHT: Direction.UP,
                Direction.DOWN: Direction.RIGHT,
                Direction.UP: Direction.LEFT,
            }.get(absolute)
        return {
            Direction.LEFT: Direction.UP,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.UP: Direction.RIGHT,
        }.get(absolute)


Direction._cart_to_direction = {
    '>': Direction.RIGHT,
    '<': Direction.LEFT,
    '^': Direction.UP,
    'v': Direction.DOWN,
}

# noinspection PyProtectedMember
Direction._direction_to_cart = {v: k for k, v in Direction._cart_to_direction.items()}

Position = Tuple[int, int]
Graph = Dict[Position, Dict[Direction, Optional[Position]]]


class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.last_turn = Direction.RIGHT

    def next_turn(self):
        return {
            Direction.LEFT: Direction.STRAIGHT,
            Direction.STRAIGHT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            None: Direction.LEFT
        }.get(self.last_turn)

    def move(self, graph: Graph):
        connections = graph[(self.y, self.x)]
        if len(connections) == 4:  # intersection
            self.last_turn = self.next_turn()
            self.direction = Direction.from_relative_direction(self.last_turn, self.direction)
        else:  # curve or straight
            opposite = self.direction.opposite()
            self.direction = next(filter(lambda d: d != opposite, connections.keys()))  # the other from two ends
            if len(graph[self.direction.apply(self.y, self.x)].keys()) < 2:  # dead end, shouldn't move
                return
        self.y, self.x = self.direction.apply(self.y, self.x)

    def __repr__(self):
        return f'Cart<y: {self.y}, x: {self.x}, dir: {self.direction}, lt: {self.last_turn}>'

    @property
    def position(self):
        return self.y, self.x

    def track_below(self):
        return {
            Direction.DOWN: '|',
            Direction.UP: '|',
            Direction.LEFT: '-',
            Direction.RIGHT: '-'
        }.get(self.direction)


def parse_tracks(raw_rails):
    rails = raw_rails.split('\n')
    carts = []
    graph: Graph = SimpleReprDefaultDict(lambda: SimpleReprDefaultDict(lambda: None))
    rails_width = max(map(len, rails))
    rails_height = len(rails)

    for y, line in enumerate(rails):
        for x, symbol in enumerate(line):
            if symbol in ['v', '^', '<', '>']:
                cart = Cart(x, y, Direction.from_cart(symbol))
                carts.append(cart)
                track = cart.track_below()
            else:
                track = symbol
            directions = {
                left_turn: [],
                '|': [Direction.UP, Direction.DOWN],
                '/': [],
                '-': [Direction.LEFT, Direction.RIGHT],
                '+': [Direction.LEFT, Direction.RIGHT, Direction.DOWN, Direction.UP],
                ' ': []

            }.get(track)
            for direction in directions:
                graph[(y, x)][direction] = direction.apply(y, x)
                graph[direction.apply(y, x)][direction.opposite()] = (y, x)
    return graph, carts


def print_rails(carts, graph: Graph):
    carts_positions: Dict[Tuple[int, int], Cart] = {cart.position: cart for cart in carts}
    tracks = list(graph.keys())
    max_x = max(map(lambda x: x[1], tracks))
    min_x = min(map(lambda x: x[1], tracks))
    max_y = max(map(lambda y: y[0], tracks))
    min_y = min(map(lambda y: y[0], tracks))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            track = graph.get((y, x), None)
            if (y, x) in carts_positions:
                cart = carts_positions[(y, x)].direction.to_cart()
                print(cart, end='')
            elif track is not None:
                track = tuple(sorted(list(track.keys())))
                track = {
                    tuple(sorted([Direction.UP, Direction.DOWN])): '|',
                    tuple(sorted([Direction.LEFT, Direction.RIGHT])): '-',
                    tuple(sorted([Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN])): '+',
                    tuple(sorted([Direction.LEFT, Direction.UP])): '/',
                    tuple(sorted([Direction.LEFT, Direction.DOWN])): '\\',
                    tuple(sorted([Direction.RIGHT, Direction.UP])): '\\',
                    tuple(sorted([Direction.RIGHT, Direction.DOWN])): '/',
                }.get(track)
                print(track, end='')
            else:
                print(' ', end='')
        print()
    print()


def part_1(graph, carts):
    carts_positions = set(cart.position for cart in carts)
    while True:
        ordered_carts = sorted(carts, key=lambda c: c.position)
        for cart in ordered_carts:
            carts_positions.remove(cart.position)
            cart.move(graph)
            pos_after_move = cart.position
            if pos_after_move in carts_positions:  # crash
                return cart.position
            else:
                carts_positions.add(pos_after_move)


def part_2(graph, carts):
    carts_positions = {cart.position: cart for cart in carts}
    carts_left = carts.copy()
    while len(carts_left) != 1:
        ordered_carts = sorted(carts_left, key=lambda c: c.position)
        invalid_carts = set()
        for cart in ordered_carts:
            if cart in invalid_carts:  # already crashed
                continue
            carts_positions.pop(cart.position)
            cart.move(graph)
            if cart.position in carts_positions:  # crash
                invalid_carts.add(carts_positions[cart.position])
                invalid_carts.add(cart)
                carts_positions.pop(cart.position)
            else:
                carts_positions[cart.position] = cart
        for invalid in invalid_carts:
            carts_left.remove(invalid)
    return carts_left[0].position


def solve():
    graph, carts = parse_tracks(raw)
    print_rails(carts, graph)
    ans = part_1(graph, carts)
    puzzle.answer_a = ','.join(map(str, reversed(ans)))
    graph, carts = parse_tracks(raw)
    ans = part_2(graph, carts)
    puzzle.answer_b = ','.join(map(str, reversed(ans)))


if __name__ == '__main__':
    solve()
