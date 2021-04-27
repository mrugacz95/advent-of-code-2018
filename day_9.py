import re
from typing import Optional, Dict

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=9)
raw = puzzle.input_data


# raw = '17 players; last marble is worth 1104 points'
# raw = '9 players; last marble is worth 25 points'

def play_game(players, last_marble, logging=False):
    marbles = [0]
    current_marble = 0
    current_player = 0
    points = [0 for _ in range(players)]
    for i in range(1, last_marble + 1):
        if logging:
            print(f'[{current_player + 1}] ', end='')
        if i % 23 == 0:
            points[current_player] += i
            current_marble = (current_marble - 7) % len(marbles)
            points[current_player] += marbles[current_marble]
            marbles.pop(current_marble)
        else:
            one_after = (current_marble + 1) % len(marbles)
            marbles.insert(one_after + 1, i)
            current_marble = one_after + 1
        if logging:
            for idx, marble in enumerate(marbles):
                if current_marble == idx:
                    print(f'({marble})', end=' ')
                else:
                    print(marble, end=' ')
            print()
        current_player = (current_player + 1) % players
    return max(points)


def play_faster(players, last_marble, logging=False):
    prev: Dict[int, Optional[int]] = {0: 0}
    next: Dict[int, Optional[int]] = {0: 0}
    current_marble = 0

    def pop(marble):
        prev_marble = prev[marble]
        next_marble = next[marble]
        next[prev_marble] = next_marble
        prev[next_marble] = prev_marble
        rv = next[marble]
        next[marble] = None
        prev[marble] = None
        return rv

    def insert(marble):
        one_after = next[current_marble]
        two_after = next[next[current_marble]]
        next[one_after] = marble
        prev[two_after] = marble
        next[marble] = two_after
        prev[marble] = one_after

    current_player = 0
    points = [0 for _ in range(players)]
    for i in range(1, last_marble + 1):
        if logging:
            print(f'[{current_player + 1}] ', end='')
        if i % 23 == 0:
            points[current_player] += i
            for j in range(7):
                current_marble = prev[current_marble]
            points[current_player] += current_marble
            current_marble = pop(current_marble)
        else:
            insert(i)
            current_marble = i
        if logging:
            printed_marble = 0
            while next[printed_marble] != 0:
                if current_marble == printed_marble:
                    print(f'({printed_marble})', end=' ')
                else:
                    print(printed_marble, end=' ')
                print()
                printed_marble = next[printed_marble]
        current_player = (current_player + 1) % players
    return max(points)


def solve():
    pattern = r'(?P<players>\d+) players; last marble is worth (?P<last_marble>\d+) points'
    m = re.match(pattern, raw)
    players = int(m.group('players'))
    last_marble = int(m.group('last_marble'))

    ans = play_game(players, last_marble)
    puzzle.answer_a = ans
    ans = play_faster(players, last_marble * 100)
    puzzle.answer_b = ans


if __name__ == '__main__':
    solve()
