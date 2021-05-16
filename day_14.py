from aocd.models import Puzzle

puzzle = Puzzle(year=2018, day=14)
puzzle_input = puzzle.input_data
brackets = [('(', ')'), ('[', ']')]


def step(recipes, elves, logging=False):
    first_recipe = recipes[elves[0]]
    second_recipe = recipes[elves[1]]
    sum_recipe = first_recipe + second_recipe
    if sum_recipe > 9:
        tens = sum_recipe // 10
        ones = sum_recipe % 10
        recipes.append(tens)
        recipes.append(ones)
    else:
        recipes.append(sum_recipe)
    for idx, elf in enumerate(elves):
        elves[idx] = (elf + recipes[elf] + 1) % len(recipes)
    if logging:
        for idx, recipe in enumerate(map(str, recipes)):
            if idx in elves:
                elf_id = elves.index(idx)
                print(brackets[elf_id][0] + str(recipe) + brackets[elf_id][1], end='')
            else:
                print(' ' + recipe, end=' ', )
        print()


def part_1(recipes_made, logging=False):
    elves = [0, 1]
    recipes = [3, 7]
    recipes_made = int(recipes_made)
    while len(recipes) < recipes_made + 10:
        step(recipes, elves, logging)
    return ''.join(map(str, recipes[recipes_made:recipes_made + 10]))


def ends_with(array, subarray):
    return array[-len(subarray):] == subarray


def part_2(recipes_seq, logging=False):
    elves = [0, 1]
    recipes = [3, 7]
    recipes_len = len(recipes)
    recipes_seq = list(map(int, list(recipes_seq)))
    while True:
        step(recipes, elves, logging)
        new_recipes_len = len(recipes)
        if recipes[-len(recipes_seq):] == recipes_seq:
            return len(recipes) - len(recipes_seq)
        # two recipes were added
        if recipes_len + 2 == new_recipes_len and \
                recipes[-len(recipes_seq) - 1:-1] == recipes_seq:
            return len(recipes) - len(recipes_seq) - 1
        recipes_len = new_recipes_len


def solve():
    assert part_1('5') == '0124515891'
    assert part_1('9') == '5158916779'
    assert part_1('18') == '9251071085'
    assert part_1('2018') == '5941429882'

    ans = part_1(puzzle_input)
    puzzle.answer_a = ans

    assert part_2('01245') == 5
    assert part_2('51589') == 9
    assert part_2('92510') == 18
    assert part_2('59414') == 2018

    assert ends_with([1, 2], [1, 2, 3, 4]) is False
    assert ends_with([-1, 0, 1, 2, 3, 4], [1, 2, 3, 4]) is True
    assert ends_with([- 1, 0, 1, 2, 3, 4], [1, 2, 3, 4]) is True
    assert ends_with([- 1, 0, 1, 2, 5, 4], [1, 2, 3, 4]) is False
    assert ends_with([- 1, 0, 1, 2, 5, 4, 7], [1, 2, 3, 4]) is False

    assert part_2('147061') == 20283721  # needed additional example

    ans = part_2(puzzle_input)
    puzzle.answer_b = ans


if __name__ == '__main__':
    solve()
