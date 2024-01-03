import abc
import heapq
from typing import List, cast, Type

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=15)

NEIGHBOURS = [
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0),
]


class Board(object):

    def __init__(self, raw_board, elf_attack=3):
        self._units = {}
        char_board = raw_board.split("\n")
        self.width = len(char_board[0])
        self.height = len(char_board)

        for y, line in enumerate(char_board):
            for x, cell in enumerate(line):
                if cell == '#':
                    obj = Wall((y, x))
                elif cell == 'G':
                    obj = Goblin((y, x))
                elif cell == 'E':
                    obj = Elf((y, x), elf_attack)
                else:
                    obj = None
                if obj is not None:
                    self._units[(y, x)] = obj

    def _in_bounds(self, pos):
        y, x = pos
        return 0 <= y < self.height and 0 <= x < self.width

    def get_unit(self, pos):
        if self._in_bounds(pos) and pos in self._units:
            return self._units[pos]
        else:
            return None

    def get_neighbours(self, pos):
        neighbours = []
        for dy, dx in NEIGHBOURS:
            ny, nx = pos[0] + dy, pos[1] + dx
            unit = self.get_unit((ny, nx))
            neighbours.append((ny, nx, unit))
        return neighbours

    def update_position(self, from_pos, to_pos):
        # print(f"move from {from_pos} to {to_pos}")
        self._units[to_pos] = self._units[from_pos]
        del self._units[from_pos]

    def __str__(self):
        result = []
        for y in range(self.height):
            line = []
            entities = []
            for x in range(self.width):
                unit = self.get_unit((y, x))
                if unit is None:
                    line.append('.')
                else:
                    entities.append(unit)
                    line.append(unit.__str__()[0])
            entities = filter(lambda x: type(x) is not Wall, entities)
            line.append('   ' + ', '.join(unit.__str__() for unit in entities))
            result.append(''.join(line))

        return '\n'.join(result)

    def simulate_round(self):
        units = list(map(lambda x: x[1], sorted(self._units.items())))
        for unit in units:
            if type(unit) is not Wall:
                has_finished = unit.step(self)
                if has_finished:
                    return True
        return False

    def get_all_entities(self):
        return list(filter(lambda x: type(x) is Goblin or type(x) is Elf, self._units.values()))

    def remove_entity(self, pos):
        del self._units[pos]

    def calculate_outcome(self, rounds):
        entities = self.get_all_entities()
        entities = filter(lambda x: not x.is_dead(), entities)
        unit_sum_hp = sum(map(lambda x: x.hp, entities))
        return rounds * unit_sum_hp


class Unit(abc.ABC):
    def __init__(self, pos):
        self.pos = pos


class Entity(Unit):
    def __init__(self, pos, ap = 3):
        super().__init__(pos)
        self.hp = 200
        self.ap = ap
        self.pos = pos

    def _get_adjacent(self, board):
        adjacent = []
        for ny, nx, unit in board.get_neighbours(self.pos):
            adjacent.append((ny, nx, unit))
        return adjacent

    def get_next_move_pos(self, board):
        closest_enemy = None
        sy, sx = self.pos
        queue = [(0, sy, sx, None, None)]
        visited = {}
        while len(queue) > 0:
            dist, node_y, node_x, prev_y, prev_x = heapq.heappop(queue)
            if (node_y, node_x) in visited:
                continue
            visited[(node_y, node_x)] = (prev_y, prev_x)

            for ny, nx, unit in board.get_neighbours((node_y, node_x)):
                if unit is None:
                    queue.append((dist + 1, ny, nx, node_y, node_x))
                if type(unit) is self.enemy() and not cast(self.enemy(), unit).is_dead():  # enemy found
                    closest_enemy = (ny, nx, dist + 1)
                    visited[(ny, nx)] = (node_y, node_x)
                    break
            if closest_enemy is not None:
                break
        if closest_enemy is None:  # not targets to reach
            return None, None, None
        ey, ex, e_dist = closest_enemy
        prev_pos = ey, ex
        while visited[prev_pos] != self.pos:
            prev_pos = visited[prev_pos]
        return prev_pos, (ey, ex), e_dist

    def step(self, board):
        if self.is_dead():
            return False

        if not any(filter(lambda x: type(x) is self.enemy(), board.get_all_entities())):  # no enemies
            return True

        next_move_pos, closest_enemy_pos, enemy_dist = self.get_next_move_pos(board)

        if closest_enemy_pos is None:  # no place to move
            return False

        # move
        if enemy_dist > 1:
            board.update_position(self.pos, next_move_pos)
            self.pos = next_move_pos

        # attack
        self.attack_phase(board)
        return False

    @abc.abstractmethod
    def enemy(self) -> 'Entity':
        pass

    def attack_phase(self, board: Board):
        enemies: List[Entity] = []
        for ny, nx, unit in board.get_neighbours(self.pos):
            if type(unit) is self.enemy():
                enemies.append(cast(self.enemy(), unit))

        if len(enemies) == 0:  # skip attacking
            return

        def enemy_priority_key(enemy):
            return enemy.hp, enemy.pos[0], enemy.pos[1]

        target = sorted(enemies, key=enemy_priority_key)[0]

        target.take_damage(self.ap, board)

    def is_dead(self):
        return self.hp <= 0

    @abc.abstractmethod
    def get_char(self):
        pass

    def __str__(self):
        return f"{self.get_char()}({self.hp})"

    def take_damage(self, dmg, board):
        self.hp -= dmg
        if self.is_dead():
            board.remove_entity(self.pos)


class Wall(Unit):

    def __str__(self):
        return '#'


class Goblin(Entity):

    def enemy(self) -> Type[Entity]:
        return Elf

    def get_char(self):
        return 'G'


class Elf(Entity):

    def __init__(self, pos, ap):
        super().__init__(pos, ap)

    def get_char(self):
        return 'E'

    def enemy(self) -> Type[Entity]:
        return Goblin


def get_order(board):
    order = []
    for line in board:
        for obj in line:
            if obj is Goblin:
                order.append(obj)
    return order


def part1(input_data):
    board = Board(input_data)
    round_count = 0
    print("Initially")
    print(board)
    print()
    while True:
        is_finish = board.simulate_round()
        if is_finish:
            break
        round_count += 1
        print(f"After {round_count} round:")
        print(board)
        print()
    return board.calculate_outcome(round_count)


def part2(input_data):
    for elf_ap in range(4, 1000):
        round_count = 0
        board = Board(input_data, elf_attack=elf_ap)
        elves = list(filter(lambda x: type(x) is Elf, board.get_all_entities()))
        while True:
            is_finish = board.simulate_round()
            if is_finish:
                break
            round_count += 1
        if not any(map(lambda elf: elf.is_dead(), elves)):
            return board.calculate_outcome(round_count)
    raise RuntimeError("No solution found")


def main():
    board = Board("#######\n"
                  "#E..G.#\n"
                  "#...#.#\n"
                  "#.G.#G#\n"
                  "#######")
    enemy = board.get_unit((1, 1))
    assert enemy.get_next_move_pos(board) == ((1, 2), (1, 4), 3)

    board = Board("#######\n"
                  "#.E...#\n"
                  "#.....#\n"
                  "#...G.#\n"
                  "#######")
    enemy = board.get_unit((1, 2))
    assert enemy.get_next_move_pos(board) == ((1, 3), (3, 4), 4)

    board = Board("#########\n"
                  "#G..G..G#\n"
                  "#.......#\n"
                  "#.......#\n"
                  "#G..E..G#\n"
                  "#.......#\n"
                  "#.......#\n"
                  "#G..G..G#\n"
                  "#########")
    print(board)
    board.simulate_round()
    print(board)
    board.simulate_round()
    print(board)
    board.simulate_round()
    print(board)

    board = Board("G....\n"
                  "..G..\n"
                  "..EG.\n"
                  "..G..\n"
                  "...G.")
    top_goblin = board.get_unit((1, 2))
    right_goblin = board.get_unit((2, 3))
    bot_goblin = board.get_unit((3, 2))
    top_goblin.hp = 4
    right_goblin.hp = 2
    bot_goblin.hp = 2
    enemy = board.get_unit((2, 2))
    enemy.attack_phase(board)
    assert right_goblin.is_dead()

    example_1 = ("#######\n"
                 "#.G...#\n"
                 "#...EG#\n"
                 "#.#.#G#\n"
                 "#..G#E#\n"
                 "#.....#\n"
                 "#######")
    assert 27730 == part1(example_1)

    example_2 = ("#######\n"
                 "#G..#E#\n"
                 "#E#E.E#\n"
                 "#G.##.#\n"
                 "#...#E#\n"
                 "#...E.#\n"
                 "#######")
    assert 36334 == part1(example_2)
    print("part1 example OK")

    example_6 = ("#########\n"
                 "#G......#\n"
                 "#.E.#...#\n"
                 "#..##..G#\n"
                 "#...##..#\n"
                 "#...#...#\n"
                 "#.G...G.#\n"
                 "#.....G.#\n"
                 "#########")
    assert 18740 == part1(example_6)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    example_1 = ("#######\n"
                 "#.G...#\n"
                 "#...EG#\n"
                 "#.#.#G#\n"
                 "#..G#E#\n"
                 "#.....#\n"
                 "#######")

    assert 4988 == part2(example_1)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
