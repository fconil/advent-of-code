"""
@author: fconil
https://adventofcode.com/2020/day/9

Day 9: Encoding Error
"""

import itertools


def load_code():
    with open("input") as f:
        instructions = [int(l.rstrip("\n")) for l in f.readlines()]  # noqa E741

    return instructions


def get_sum(window):
    return set(map(sum, itertools.combinations(window, 2)))


def find_invalid_number(instructions, preamble):
    length = len(instructions)

    start = 0
    end = preamble

    idx = preamble

    while idx < length:
        if instructions[idx] not in get_sum(instructions[start:end]):
            break

        start += 1
        end += 1
        idx += 1

    return idx


if __name__ == "__main__":
    instructions = load_code()

    idx = find_invalid_number(instructions, 25)

    if idx < len(instructions):
        print(f"[{idx}]: {instructions[idx]} is not the sum of the previous window")
    else:
        print("No invalid number found")
