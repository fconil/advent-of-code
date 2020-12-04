"""
https://adventofcode.com/2020/day/1

https://docs.python.org/3/library/itertools.html#itertools.combinations
"""
import itertools

with open("input", "r") as f:
    l_input = [int(l.rstrip("\n")) for l in f.readlines()]  # noqa E741

for comb in itertools.combinations(l_input, 3):
    if sum(comb) == 2020:
        v1, v2, v3 = comb
        print(f"{v1}+{v2}+{v3} = {v1+v2+v3}, {v1}*{v2}*{v3} = {v1*v2*v3}")
