#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: fconil
https://adventofcode.com/2020/day/4

byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)
"""
from collections import namedtuple
import logging

logger = logging.getLogger(__name__)

Passport = namedtuple(
    "Passport", ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
)

PASSPORT_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}


def load_batch():
    """"""
    with open("input", "r") as f:
        l_input = [l.rstrip("\n") for l in f.readlines()]  # noqa E741

    p_list = []
    passport = []

    for line in l_input:
        logger.debug(f"Line : {line}")
        if len(line) == 0:
            logger.debug("empty line, changing passport")
            p_list.append(passport)
            passport = []
        else:
            elts = line.split(" ")
            logger.debug(f"Put {elts} in passport")
            passport.extend(elts)

    p_list.append(passport)

    return p_list


def format_passport(r_passport):
    f_passport = {}

    for elts in r_passport:
        field, value = elts.split(":")

        f_passport[field] = value

    return f_passport


def check_passport(passport):
    valid = False

    diff = PASSPORT_FIELDS.difference(set(passport.keys()))

    logger.debug(f"diff: {diff} for passport: {passport}")

    if (len(diff) == 0) or (len(diff) == 1) and (diff.pop() == "cid"):
        valid = True
    return valid


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)

    nb_valid_passports = 0

    passport_list = load_batch()

    for raw_passport in passport_list:
        logger.warning(f"Formatting {raw_passport}")

        passport = format_passport(raw_passport)

        if check_passport(passport):
            nb_valid_passports += 1

    print(f"nb_passports: {len(passport_list)} => nb_valid: {nb_valid_passports}")
