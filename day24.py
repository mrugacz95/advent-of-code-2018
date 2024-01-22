import re
from collections import defaultdict
from copy import copy
from functools import cmp_to_key, reduce

from aocd.models import Puzzle
from tqdm import tqdm

puzzle = Puzzle(year=2018, day=24)


class Group:
    def __init__(self, army, id, units, hp, immunities, weaknesses, ap, attack_type, initiative):
        self.id = id
        self.target = None
        self.attacker = None
        self.army = army
        self.initiative = initiative
        self.attack_type = attack_type
        self.ap = ap
        self.weaknesses = weaknesses
        self.immune = immunities
        self.hp = hp
        self.units = units

    def effective_power(self):
        return self.units * self.ap

    def calc_dmg(self, attacker):
        attacker_ep = attacker.effective_power()
        if attacker.attack_type in self.immune:
            return 0
        if attacker.attack_type in self.weaknesses:
            return 2 * attacker_ep
        return attacker_ep

    def is_alive(self):
        return self.units > 0

    def receive_dmg(self, attacker, debug):
        dmg = self.calc_dmg(attacker)
        units_lost = dmg // self.hp
        units_lost = min(units_lost, self.units)
        self.units -= units_lost
        if debug:
            print(f"{attacker.army} group {attacker.id} attacks defending group {self.id}, killing "
                  f"{units_lost} units (dmg={dmg}, hp={self.hp})")

    def __repr__(self):
        result = f"{self.units} units each with {self.hp} hit points "
        if self.immune or self.weaknesses:
            result += ('(' +
                       (f"immune to {', '.join(self.immune)};" if self.immune else "") +
                       (f"weak to {', '.join(self.weaknesses)}" if self.weaknesses else "") +
                       ') ')
        result += f"with an attack that does {self.ap} {self.attack_type} damage at initiative {self.initiative}"
        return result

    def __eq__(self, other):
        return self.army == other.army and self.id == other.id and self.units == other.units


def parse(input_data):
    armies = input_data.split("\n\n")
    groups = []
    for army in armies:
        lines = army.split("\n")
        for id, groups_definition in enumerate(lines[1:]):
            groups_definition = ''.join(groups_definition)
            match = re.findall(
                r"(\d+) units each with (\d+) hit points (\([a-z,; ]+\) )?with an attack that does (\d+) ([a-z]+) damage at initiative (\d+) ?",
                groups_definition)
            units, hp, hardiness, ap, attack_type, initiative = match[0]
            immunities = re.findall(r"immune to ([a-z, ]+)", hardiness)
            weaknesses = re.findall(r"weak to ([a-z, ]+)", hardiness)
            hp = int(hp)
            if weaknesses:
                weaknesses = weaknesses[0].split(", ")
            else:
                weaknesses = []
            if immunities:
                immunities = immunities[0].split(", ")
            else:
                immunities = []
            ap = int(ap)
            units = int(units)
            initiative = int(initiative)
            groups.append(Group(lines[0][:-1], id + 1, units, hp, immunities, weaknesses, ap, attack_type, initiative))
    return groups


def get_max(iter, key):
    if len(iter) == 0:
        return None
    values = list(map(lambda o: key(o), iter))
    max_value = max(values)
    return [obj for obj, v in zip(iter, values) if v == max_value]


def select_target(groups, debug):
    for group in groups:
        group.target = None
        group.attacker = None

    def order_cmp(lhs, rhs):
        lhs_ep = lhs.effective_power()
        rhs_ep = rhs.effective_power()
        if lhs_ep != rhs_ep:
            return 1 if lhs_ep < rhs_ep else -1
        else:
            return 1 if lhs.initiative > rhs.initiative else -1

    choose_order = sorted(groups, key=cmp_to_key(order_cmp))

    for group in choose_order:
        enemies = list(filter(lambda g: group.army != g.army, choose_order))
        targets = list(filter(lambda g: g.calc_dmg(group) > 0 and g.attacker is None, enemies))
        if debug:
            for enemy in targets:
                print(f"{group.army} group {group.id} would deal defending group"
                      f" {enemy.id} {enemy.calc_dmg(group)} damage")

        candidates = get_max(targets, lambda t: t.calc_dmg(group))
        if candidates is None:
            continue
        if len(candidates) == 1:
            target = candidates[0]
        else:
            most_powerful_candidates = get_max(candidates, lambda e: e.effective_power())
            if len(most_powerful_candidates) == 1:
                target = most_powerful_candidates[0]
            else:
                highest_initiative = get_max(most_powerful_candidates, lambda e: e.initiative)
                assert len(highest_initiative) == 1
                target = highest_initiative[0]
        group.target = target
        target.attacker = group
    if debug:
        print()


def attack(groups, debug):
    initiative_order = sorted(groups, key=lambda g: g.initiative, reverse=True)
    for group in initiative_order:
        if group.is_alive() and group.target is not None and group.target.is_alive():
            group.target.receive_dmg(group, debug)


def get_armies(groups):
    armies = set()
    for group in groups:
        armies.add(group.army)
    return armies


def fight(groups, debug):
    select_target(groups, debug)
    attack(groups, debug)

    groups_left = []
    for group in groups:
        if group.is_alive():
            groups_left.append(group)
    return groups_left, len(get_armies(groups_left)) == 1


def print_armies(groups):
    armies = get_armies(groups)
    for army in armies:
        army_groups = list(filter(lambda g: g.army == army, groups))
        print(f"{army}:")
        for group in army_groups:
            print(f"Group {group.id} contains {group.units} units")
    print()


# def is_infinite(groups):
#     armies = defaultdict(list)
#     for group in groups:
#         armies[group.army].append(group)
#     a1, a2 = armies.keys()
#     for g1 in armies[a1]:
#         for g2 in armies[a2]:
#             if g2.attack_type not in g1.immune:
#                 return False
#             if g1.attack_type not in g2.immune:
#                 return False
#     return True


def simulate(groups, debug):
    while True:
        if debug: print_armies(groups)
        # if is_infinite(groups):
        #     return None
        fighters = [copy(g) for g in groups]
        fighters, finished = fight(fighters, debug)
        if groups == fighters:  # nothing changed
            return None
        groups = fighters
        if finished:
            break
    return groups


def calc_units_left(groups):
    return sum(map(lambda g: g.units, groups))


def part1(input_data, debug=False):
    groups = parse(input_data)
    groups_left = simulate(groups, debug)
    return calc_units_left(groups_left)


def part2(input_data, debug=False):
    groups = parse(input_data)
    boost = 0
    progress = tqdm()
    while True:
        boost += 1
        progress.update()
        boosted_groups = []
        for group in groups:
            new_group = copy(group)
            if new_group.army == "Immune System":
                new_group.ap += boost
            boosted_groups.append(new_group)
        groups_left = simulate(boosted_groups, debug)
        if groups_left is None:  # infinite fight
            continue
        immune_system_groups = list(filter(lambda g: g.army == "Immune System", groups_left))
        if len(immune_system_groups) > 0:
            break
    progress.clear()
    progress.close()
    return calc_units_left(groups_left)


def main():
    example = ("Immune System:\n"
               "17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2\n"
               "989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3\n"
               "\n"
               "Infection:\n"
               "801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1\n"
               "4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4")
    assert 5216 == part1(example, True)
    print("part1 example OK")

    puzzle.answer_a = part1(puzzle.input_data)
    print("part1 OK")

    assert 51 == part2(example)
    print("part2 example OK")

    puzzle.answer_b = part2(puzzle.input_data)
    print("part2 OK")


if __name__ == '__main__':
    main()
