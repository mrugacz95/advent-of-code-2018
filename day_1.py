from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=1)


def part1():
    puzzle.answer_a = sum(map(int, puzzle.input_data.split()))


def part2():
    frequencies = set()
    current_freq = 0
    freq_list = list(map(int , puzzle.input_data.split()))
    current_freq_idx = 0
    while True:
        next_freq = freq_list[current_freq_idx % len(freq_list)]
        current_freq_idx += 1
        current_freq += next_freq
        if current_freq in frequencies:
            ans = current_freq
            break
        frequencies.add(current_freq)
    puzzle.answer_b = str(ans)


if __name__ == '__main__':
    # part1()
    part2()
