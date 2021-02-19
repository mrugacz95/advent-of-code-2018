import re
from collections import defaultdict
from datetime import datetime
from enum import Enum

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=4)


class Action:
    def __init__(self, date, action, guard_id):
        self.guard_id = guard_id
        self.type = {
            'falls asleep': Type.SLEEP,
            'wakes up': Type.WAKE_UP
        }.get(action, Type.START)
        self.date = date


class Type(Enum):
    START = 0
    WAKE_UP = 1
    SLEEP = 2


def parse(line):
    pattern = r"\[(?P<datetime>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}))\] " \
              r"(?P<action>(Guard #(?P<guard_id>\d+) begins shift|falls asleep|wakes up))"
    match = re.match(pattern, line)
    dt = match.group("datetime")
    dt = datetime.strptime(dt, '%Y-%m-%d %H:%M')
    action = match.group("action")
    guard_id = match.group('guard_id')
    return Action(dt, action, guard_id)


raw_data = puzzle.input_data
parsed_data = sorted(map(parse, raw_data.split("\n")), key=lambda a: a.date)


def part_1():
    guard_id = None
    time_slept = defaultdict(lambda: [0] * 60)
    for action_id, action in enumerate(parsed_data):
        if action.type == Type.START:
            guard_id = action.guard_id
        if action.type == Type.WAKE_UP:
            for min in range(parsed_data[action_id - 1].date.minute, action.date.minute):
                time_slept[guard_id][min] += 1
    most_sleepy_guard_id = max(time_slept.items(), key=lambda x: sum(x[1]))[0]
    max_minute = max(range(len(time_slept[most_sleepy_guard_id])), key=lambda x: time_slept[most_sleepy_guard_id][x])
    puzzle.answer_a = max_minute * int(most_sleepy_guard_id)


def part_2():
    guard_id = None
    time_slept = [defaultdict(int) for _ in range(60)]
    most_sleepy_guard_id = None
    max_minute = None
    slept_over_minute_count = 0
    for action_id, action in enumerate(parsed_data):
        if action.type == Type.START:
            guard_id = action.guard_id
        if action.type == Type.WAKE_UP:
            for minute in range(parsed_data[action_id - 1].date.minute, action.date.minute):
                time_slept[minute][guard_id] += 1
                if slept_over_minute_count < time_slept[minute][guard_id]:
                    slept_over_minute_count = time_slept[minute][guard_id]
                    most_sleepy_guard_id = guard_id
                    max_minute = minute
    puzzle.answer_b = max_minute * int(most_sleepy_guard_id)


if __name__ == '__main__':
    part_1()
    part_2()
