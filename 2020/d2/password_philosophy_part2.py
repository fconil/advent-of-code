"""
https://adventofcode.com/2020/day/2
"""

from collections import namedtuple
import logging

logger = logging.getLogger(__name__)

Rule = namedtuple("Rule", ["letter", "f_pos", "s_pos"])


def check_password(rule, password):
    f_letter = password[rule.f_pos - 1]
    s_letter = password[rule.s_pos - 1]

    return (f_letter == rule.letter) ^ (s_letter == rule.letter)


def get_rule(rule_text):
    times, letter = rule_text.split(" ")
    f_pos, s_pos = times.split("-")
    f_pos = int(f_pos)
    s_pos = int(s_pos)

    return Rule(letter, f_pos, s_pos)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)

    with open("input", "r") as f:
        l_input = [l.rstrip("\n") for l in f.readlines()]  # noqa E741

    valid_passwords = 0

    for line in l_input:
        rule_text, password = line.split(":")

        password = password.strip()
        rule = get_rule(rule_text)

        logger.debug("base: %s", line)
        logger.debug(f"rule: {rule}, password: {password}")

        if check_password(rule, password):
            valid_passwords += 1

    print(f"Valid passwords: {valid_passwords} on {len(l_input)}")
