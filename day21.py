import enum
from typing import Callable

from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=21)


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
    exec_counter = 0
    while True:
        if ip_break == ip:
            break
        if reg[-1] is False:
            break
        if ip_register is not None:
            reg[ip_register] = ip
        opcode, a, b, c = program[ip]
        exec_counter += 1
        opcode.get_operator()(reg, a, b, c)
        # print(ip, program[ip], reg)
        if ip_register is not None:
            ip = reg[ip_register]
        ip += 1
        if ip < 0 or ip >= len(program):
            break
    return exec_counter


def part1(input_data):
    program, ip_register = parse(input_data)
    reg = [0, 0, 0, 0, 0, 0]
    simulate_computer(program, ip_register, reg, ip_break=29)  # comparison with reg[0] is in line 29
    reg_0 = reg[1]
    print(reg_0)
    reg = [reg_0, 0, 0, 0, 0, 0]
    counter = simulate_computer(program, ip_register, reg)
    print(f"Executed {counter} operations")
    return reg_0


def part2_simulation():
    x1, x4, x5 = 0, 0, 0
    while True:
        x4 = x1 | 65536
        x1 = 16298264
        while True:
            x5 = 255 & x4
            x1 += x5
            x1 &= 16777215
            x1 *= 65899
            x1 &= 16777215
            if 256 > x4:
                yield x1
                break
            x5 = x4 // 256
            x4 = x5


def part2(input_data):
    numbers = []
    generator = part2_simulation()
    while True:
        number = next(generator)
        if number in numbers:
            break
        numbers.append(number)
    print(f"Last number is {numbers[-1]}")
    return numbers[-1]


def main():
    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
