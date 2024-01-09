import enum
from typing import Callable

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=19)


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


class Opcode(enum.StrEnum):
    IP = "#ip"
    ADDR = "addr"
    ADDI = "addi"
    MULR = "mulr"
    MULI = "muli"
    BANR = "andr"
    BANI = "bani"
    BORR = "borr"
    BORI = "bori"
    SETR = "setr"
    SETI = "seti"
    GTIR = "gtir"
    GTRI = "gtri"
    GTRR = "gtrr"
    EQIR = "eqir"
    EQRI = "eqri"
    EQRR = "eqrr"

    def get_operator(self) -> Callable[[[int], int, int, int], int]:
        if self == Opcode.IP:
            raise RuntimeError("No operator for #ip")
        return {
            self.ADDR: addr,
            self.ADDI: addi,
            self.MULR: mulr,
            self.MULI: muli,
            self.BANR: banr,
            self.BANI: bani,
            self.BORR: borr,
            self.BORI: bori,
            self.SETR: setr,
            self.SETI: seti,
            self.GTIR: gtir,
            self.GTRI: gtri,
            self.GTRR: gtrr,
            self.EQIR: eqir,
            self.EQRI: eqri,
            self.EQRR: eqrr,
        }.get(self)


def parse(input_data):
    program = []
    ip_register = None
    for line in input_data.split("\n"):
        opcode = line.split(" ")[0]
        opcode = Opcode(opcode)
        if opcode is Opcode.IP:
            _, reg = line.split(" ")
            ip_register = int(reg)
        else:
            _, a, b, c = line.split(" ")
            program.append((opcode, int(a), int(b), int(c)))
    return program, ip_register


def simulate_computer(program, ip_register, reg, ip_break=None):
    ip = 0
    while True:
        if ip_break == ip:
            return
        if ip_register is not None:
            reg[ip_register] = ip
        opcode, a, b, c = program[ip]
        opcode.get_operator()(reg, a, b, c)
        # print(ip, program[ip], reg)
        if ip_register is not None:
            ip = reg[ip_register]
        ip += 1
        if ip < 0 or ip >= len(program):
            break


def part1(input_data):
    program, ip_register = parse(input_data)
    reg = [0, 0, 0, 0, 0, 0]
    simulate_computer(program, ip_register, reg)
    return reg[0]


def divisors(number):
    yield 1
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            yield i
    yield number


def part2(input_data):
    program, ip_register = parse(input_data)
    reg = [1, 0, 0, 0, 0, 0]
    simulate_computer(program, ip_register, reg, ip_break=4)
    return sum(divisors(reg[3]))


def main():
    assert 6 == part1(puzzle.examples[0].input_data)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
