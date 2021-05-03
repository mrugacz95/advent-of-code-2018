from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=11)
raw = puzzle.input_data


def one_cell_power(x, y, serial_number):
    rack_id = x + 10
    power_lvl = rack_id * y
    power_lvl += serial_number
    power_lvl *= rack_id
    power_lvl = power_lvl // 100 % 10
    return power_lvl - 5


def part_1(serial_number):
    grid_size = 300
    grid = {}
    max_value = float("-inf")
    max_position = None
    for x in range(1, grid_size + 1):
        for y in range(1, grid_size + 1):
            grid[(x, y)] = one_cell_power(x, y, serial_number)
    for x in range(1, grid_size + 1 - 3):
        for y in range(1, grid_size + 1 - 3):
            total_power = 0
            for dx in range(3):
                for dy in range(3):
                    total_power += grid[(x + dx, y + dy)]
            if total_power > max_value:
                max_value = total_power
                max_position = (x, y)
    return max_position


def max_sum_subarray(arr, size):
    current_sum = 0
    for i in range(size):
        current_sum += arr[i]
    max_sum = current_sum
    max_position = 0
    for i in range(len(arr) - size):
        current_sum -= arr[i]
        current_sum += arr[i + size]
        if current_sum > max_sum:
            max_sum = current_sum
            max_position = i + 1
    return max_position, max_sum


def part_2(serial_number):
    grid_size = 300

    def calc_all_cells():
        cells = [[0] * grid_size for _ in range(grid_size)]
        for x in range(grid_size):
            for y in range(grid_size):
                cells[y][x] = one_cell_power(x + 1, y + 1, serial_number)
        return cells

    max_sum = -float('inf')
    max_left = None
    max_top = None
    max_square_size = None
    all_cells = calc_all_cells()
    for left in range(grid_size):
        for right in range(left + 1, grid_size + 1):
            square_size = right - left
            row_sums = [sum(all_cells[row][left: right]) for row in range(grid_size)]
            current_pos, current_max = max_sum_subarray(row_sums, square_size)
            if current_max > max_sum:
                max_sum = current_max
                max_top = current_pos
                max_left = left
                max_square_size = square_size
    return max_left + 1, max_top + 1, max_square_size


def solve():
    assert one_cell_power(3, 5, 8) == 4
    assert one_cell_power(122, 79, 57) == -5
    assert one_cell_power(217, 196, 39) == 0
    assert one_cell_power(101, 153, 71) == 4

    assert part_1(18) == (33, 45)
    assert part_1(42) == (21, 61)

    assert max_sum_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4], 4) == (3, 6)
    assert max_sum_subarray([-2, -3, 4, -1, -2, 1, 5, -3], 5) == (2, 7)

    assert part_2(18) == (90, 269, 16)
    assert part_2(42) == (232, 251, 12)

    serial_number = int(raw)

    ans = part_1(serial_number)
    puzzle.answer_a = ','.join(map(str, ans))

    ans = part_2(serial_number)
    puzzle.answer_b = ','.join(map(str, ans))


if __name__ == '__main__':
    solve()
