#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:33:28 2020
@author: fconil
https://adventofcode.com/2020/day/3
"""
import logging

logger = logging.getLogger(__name__)


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

        return self.map[position.line][index]


if __name__ == "__main__":
    logger.setLevel(logging.WARNING)
    # logger.setLevel(logging.INFO)
    # logger.setLevel(logging.DEBUG)

    step_down = 1
    step_right = 3

    nb_tree = 0

    with open("input", "r") as f:
        l_input = [l.rstrip("\n") for l in f.readlines()]  # noqa E741

    t_map = Map(l_input)
    t = Toboggan(step_down, step_right, t_map.height, t_map.width)

    # TODO : erreur de partir de 1
    for row in range(1, t_map.height):
        t.lead()
        elt = t_map.is_tree(t)

        logger.debug(f"Toboggan: ({t.line}, {t.col}) = {elt}")

        if elt == "#":
            nb_tree += 1

    print(f"Number of trees: {nb_tree}")
