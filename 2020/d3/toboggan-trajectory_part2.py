#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:33:28 2020
@author: fconil
https://adventofcode.com/2020/day/3
"""
from functools import reduce
from collections import namedtuple
import logging
from operator import mul

logger = logging.getLogger(__name__)

Slope = namedtuple("Slope", ["step_right", "step_down"])


class Toboggan:
    def __init__(self, step_down, step_right, height, width):
        self.line = 0
        self.col = 0
        self.step_down = step_down
        self.step_right = step_right
        self.height = height
        self.width = width

    def lead(self):
        self.col += self.step_right

        # Bottom of the map is checked elsewhere
        self.line += self.step_down


class Map:
    def __init__(self, input):
        self.map = input
        self.height = len(input)
        self.width = len(input[0])

    def is_tree(self, position):
        index = position.col

        if position.col >= self.width:
            index = position.col % self.width

        logger.info(f"position.col: {position.col}, index:{index}")

        return self.map[position.line][index]


def walk_the_map(slope):
    nb_tree = 0

    with open("input", "r") as f:
        l_input = [l.rstrip("\n") for l in f.readlines()]  # noqa E741

    t_map = Map(l_input)
    t = Toboggan(slope.step_down, slope.step_right, t_map.height, t_map.width)

    for row in range(slope.step_down, t_map.height, slope.step_down):
        t.lead()

        logger.info(f"row: {row}, t.line:{t.line}, t.col:{t.col}")

        elt = t_map.is_tree(t)

        logger.debug(f"Toboggan: ({t.line}, {t.col}) = {elt}")

        if elt == "#":
            nb_tree += 1

    print(
        f"Number of trees: {nb_tree} for Right:{slope.step_right}, "
        f"Down:{slope.step_down}"
    )

    return nb_tree


if __name__ == "__main__":
    logger.setLevel(logging.WARNING)
    # logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)

    slopes = [Slope(1, 1), Slope(3, 1), Slope(5, 1), Slope(7, 1), Slope(1, 2)]

    nb_list = []

    for slope in slopes:
        logger.info(f"Slope => Right:{slope.step_right}, Down:{slope.step_down}")
        nb_list.append(walk_the_map(slope))

    result = reduce(mul, nb_list)
    print(f"nb_list: {nb_list} => result: {result}")
