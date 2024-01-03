from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=16)


def parse(input_data):
    observations, program = input_data.split("\n\n\n\n")
    parsed_observations = []
    for observation in observations.split("\n\n"):
        lines = observation.split("\n")
        before = list(map(int, lines[0][9:-1].split(", ")))
        opcode = list(map(int, lines[1].split(" ")))
        after = list(map(int, lines[2][9:-1].split(", ")))
        parsed_observations.append((before, opcode, after))
    parsed_program = []
    for line in program.split("\n"):
        parsed_program.append(list(map(int, line.split(" "))))
    return parsed_observations, parsed_program


def addr(reg, a, b, c):
    reg[c] = reg[a] + reg[b]


def addi(reg, a, b, c):
    reg[c] = reg[a] + b


def mulr(reg, a, b, c):
    reg[c] = reg[a] * reg[b]


def muli(reg, a, b, c):
    reg[c] = reg[a] * b


def banr(reg, a, b, c):
    reg[c] = reg[a] & reg[b]


def bani(reg, a, b, c):
    reg[c] = reg[a] & b


def borr(reg, a, b, c):
    reg[c] = reg[a] | reg[b]


def bori(reg, a, b, c):
    reg[c] = reg[a] | b


def setr(reg, a, b, c):
    reg[c] = reg[a]


def seti(reg, a, b, c):
    reg[c] = a


def gtir(reg, a, b, c):
    reg[c] = 1 if a > reg[b] else 0


def gtri(reg, a, b, c):
    reg[c] = 1 if reg[a] > b else 0


def gtrr(reg, a, b, c):
    reg[c] = 1 if reg[a] > reg[b] else 0


def eqir(reg, a, b, c):
    reg[c] = 1 if a == reg[b] else 0


def eqri(reg, a, b, c):
    reg[c] = 1 if reg[a] == b else 0


def eqrr(reg, a, b, c):
    reg[c] = 1 if reg[a] == reg[b] else 0


operations = [
    addr, addi,
    mulr, muli,
    banr, bani,
    borr, bori,
    setr, seti,
    gtir, gtri, gtrr,
    eqir, eqri, eqrr
]


def part1(input_data):
    observations, _ = parse(input_data)
    result = 0
    for before, opcode, after in observations:
        matches = 0
        for operation in operations:
            code, a, b, c = opcode
            reg = before.copy()
            operation(reg, a, b, c)
            if reg == after:
                matches += 1
        if matches >= 3:
            result += 1
    return result


def part2(input_data):
    observations, program = parse(input_data)
    mapping = {}
    while len(mapping) != len(operations):
        for before, opcode, after in observations:
            matches = []
            code, a, b, c = opcode
            for op_idx, operation in enumerate(operations):
                if op_idx in mapping.values():
                    continue
                reg = before.copy()
                operation(reg, a, b, c)
                if reg == after:
                    matches.append(op_idx)
            if len(matches) == 1:
                mapping[code] = matches[0]
    print(f"Mapping found: {mapping}")
    reg = [0, 0, 0, 0]
    for code, a, b, c in program:
        operation = operations[mapping[code]]
        operation(reg, a, b, c)
    return reg[0]


def main():
    example = ("Before: [3, 2, 1, 1]\n"
               "9 2 1 2\n"
               "After:  [3, 2, 2, 1]\n\n\n\n"
               "1 1 1 1")
    assert 1 == part1(example)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
