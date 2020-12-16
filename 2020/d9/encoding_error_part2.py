"""
@author: fconil
https://adventofcode.com/2020/day/9

Day 9: Encoding Error
"""
import itertools
import logging

logger = logging.getLogger(__name__)


def load_code():
    with open("input") as f:
        instructions = [int(l.rstrip("\n")) for l in f.readlines()]  # noqa E741

    return instructions


def get_sum(window):
    return set(map(sum, itertools.combinations(window, 2)))


def find_invalid_number(instructions, preamble):
    length = len(instructions)

    # window = Window(0, preamble, preamble)

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


def find_sum(instructions, idx):
    searched = instructions[idx]

    start = idx

    for end in range(idx - 1, 1, -1):
        start = end
        computed = 0
        logger.debug(f"\n[for] end: {end}")
        while (start >= 1) and (computed < searched):
            start -= 1
            computed = sum(instructions[start:end])
            logger.debug(
                f"[while] start: {start}, end: {end}, "
                f"computed: {computed}, searched: {searched}"
            )

        if computed == searched:
            break

    return start, end


if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARNING)
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)

    instructions = load_code()

    idx = find_invalid_number(instructions, 25)

    if idx < len(instructions):
        print(f"[{idx}]: {instructions[idx]} is not the sum of the previous window")

        start, end = find_sum(instructions, idx)
        print(f"start: {start}, end: {end}")

        s_min = min(instructions[start:end])
        s_max = max(instructions[start:end])

        print(f"min: {s_min}, max: {s_max}, sum: {s_min + s_max}")
    else:
        print("No invalid number found")
