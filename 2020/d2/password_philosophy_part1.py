"""
https://adventofcode.com/2020/day/2
"""

from collections import namedtuple
import logging

logger = logging.getLogger(__name__)

Rule = namedtuple("Rule", ["letter", "t_min", "t_max"])


def check_password(rule, password):
    nb_letter = password.count(rule.letter)
    if (nb_letter >= rule.t_min) and (nb_letter <= rule.t_max):
        return True

    return False


def get_rule(rule_text):
    times, letter = rule_text.split(" ")
    t_min, t_max = times.split("-")
    t_min = int(t_min)
    t_max = int(t_max)

    return Rule(letter, t_min, t_max)


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
