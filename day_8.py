from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=8)
raw = puzzle.input_data


# raw = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"""

def solve():
    data = list(map(int, raw.split(" ")))

    # Part 1
    tree = iter(data)

    def parse_node(iterator):
        metadata_sum = 0
        nodes_count = next(iterator)
        metadata_count = next(iterator)
        for i in range(nodes_count):
            metadata_sum += parse_node(iterator)
        for i in range(metadata_count):
            metadata_sum += next(iterator)
        return metadata_sum

    ans = parse_node(tree)
    puzzle.answer_a = ans

    # Part 2
    tree = iter(data)

    def parse_node(iterator):
        metadata_sum = 0
        nodes_count = next(iterator)
        metadata_count = next(iterator)

        child_nodes = []
        for i in range(nodes_count):
            child_nodes.append(parse_node(iterator))
        for i in range(metadata_count):
            entry = next(iterator)
            if nodes_count == 0:
                metadata_sum += entry
            elif 0 < entry <= nodes_count:
                metadata_sum += child_nodes[entry - 1]
        return metadata_sum

    ans = parse_node(tree)
    puzzle.answer_b = ans


if __name__ == '__main__':
    solve()
