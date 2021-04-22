import re
from collections import defaultdict, deque
from heapq import heappush, heappop, nsmallest
from typing import List, Dict, Optional
from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=7)
raw = puzzle.input_data

# raw = """Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin."""

pattern = r"Step (?P<before>[A-Z]) must be finished before step (?P<after>[A-Z]) can begin\."


def calc_id_degree(graph):
    in_degree = {node: 0 for node in graph.keys()}

    for node, neighbours in graph.items():
        for neighbour in neighbours:
            in_degree[neighbour] += 1

    return in_degree


def topological_sort(graph: Dict[str, List[str]]):
    order = deque()
    in_degree = calc_id_degree(graph)

    queue = []
    for node, count in in_degree.items():
        if count == 0:
            heappush(queue, node)

    while len(queue) > 0:
        current = heappop(queue)
        order.append(current)
        for neighbour in graph[current]:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                heappush(queue, neighbour)
    return order


def solve():
    graph = defaultdict(list)
    for line in raw.split("\n"):
        match = re.match(pattern, line)
        before = match.group("before")
        after = match.group("after")
        graph[before].append(after)
        if after not in graph:
            graph[after] = []

    # Part 1

    order = topological_sort(graph)
    puzzle.answer_a = ''.join(order)

    # Part 2

    workers_number = 5
    task_additional_time = 60
    inv_graph = defaultdict(list)
    for task_id, next_tasks in graph.items():
        for next_task in next_tasks:
            inv_graph[next_task].append(task_id)

    def task_duration(task_name: str):
        return ord(task_name[0]) - ord('A') + task_additional_time + 1

    in_degree = calc_id_degree(graph)
    tasks_available_time = {key: None for key in graph.keys()}
    tasks_finish_time = {key: None for key in graph.keys()}
    for task_id, task_in_degree in in_degree.items():
        if task_in_degree == 0:
            tasks_available_time[task_id] = 0
    duration = {task: task_duration(task) for task in graph.keys()}
    workers = [0 for _ in range(workers_number)]

    def get_next_task():
        all_tasks = graph.keys()
        available_tasks = list(filter(lambda i: tasks_available_time[i] is not None, all_tasks))
        not_finished_tasks = list(filter(lambda i: tasks_finish_time[i] is None, available_tasks))
        min_available_time = min([tasks_available_time[i] for i in not_finished_tasks])
        earliest_tasks = list(filter(lambda i: tasks_available_time[i] == min_available_time, not_finished_tasks))
        lexicographical_tasks = sorted(earliest_tasks)
        return lexicographical_tasks[0]

    def is_available(task_id):
        return all([tasks_finish_time[prev_task] is not None for prev_task in inv_graph[task_id]])

    while None in tasks_finish_time.values():
        next_task = get_next_task()
        current_time = tasks_available_time[next_task]
        next_worker_id = min(range(workers_number), key=lambda x: workers[x])
        current_time = max(workers[next_worker_id], current_time)
        task_finish_time = current_time + duration[next_task]
        tasks_finish_time[next_task] = task_finish_time
        workers[next_worker_id] = tasks_finish_time[next_task]
        for successor in graph[next_task]:
            if is_available(successor):
                tasks_available_time[successor] = task_finish_time

    ans = max(tasks_finish_time.values())
    puzzle.answer_b = ans

if __name__ == '__main__':
    solve()
