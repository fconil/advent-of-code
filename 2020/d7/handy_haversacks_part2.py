"""
@author: fconil
https://adventofcode.com/2020/day/7

Day 7: Handy Haversacks

Helpers:
- https://docs.python.org/3.8/library/re.html
- https://docs.python.org/3.8/howto/regex.html#regex-howto
- https://pymotw.com/3/re/index.html
- https://regexper.com/
- https://learnbyexample.github.io/python-regex-cheatsheet/
"""
# from pprint import pprint
import logging
import re

logger = logging.getLogger(__name__)


def parse_bag_rules():
    with open("input") as f:
        l_input = f.readlines()

    # Do not want to build a complex regexp for subgroups
    bag_rules_parts = [
        r"^(?P<bag_color>\w+\s\w+)",
        r"bags contain",
        r"(?P<bag_content>.*)",
    ]
    bag_rules_RE = r"\s+".join(bag_rules_parts)
    bag_rules_pattern = re.compile(bag_rules_RE)

    bag_rules = {}

    for line in l_input:
        logger.debug(f"Parse line: {line}")

        m = bag_rules_pattern.match(line)
        if m is not None:
            logger.debug(f"{m.groupdict()}")
            bag_color = m.groupdict()["bag_color"]
            bag_rules[bag_color] = m.groupdict()
            del bag_rules[bag_color]["bag_color"]
        else:
            logger.debug("Pattern did not match the line")

    # Improve bag content parsing
    bag_rules_parts = [
        r"^(?P<bag_color>\w+\s\w+)",
        r"bags contain",
        r"(?P<bag_content>.*)",
    ]
    bag_rules_RE = r"\s+".join(bag_rules_parts)
    bag_rules_pattern = re.compile(bag_rules_RE)
    for rule in bag_rules.values():
        bag_content = rule["bag_content"].strip(".")
        content = [bag.strip() for bag in bag_content.split(",")]

        bag_content_RE = r"^(?P<nb>\d+)\s(?P<bag_color>\w+\s\w+)\sbag[s]?$"
        if (len(content) == 1) and re.match("no other bags", content[0]) is not None:
            rule["nb_bag_types"] = 0
        else:
            rule["nb_bag_types"] = len(content)
            rule["contains"] = {}
            total_bags = 0

            for element in content:
                m = re.match(bag_content_RE, element)
                if m is not None:
                    nb_bags = int(m.groupdict()["nb"])
                    rule["contains"][m.groupdict()["bag_color"]] = nb_bags
                    total_bags += nb_bags

            rule["nb_total_bags"] = total_bags

        del rule["bag_content"]

    # pprint(bag_rules)
    logger.debug(f"Rule dict: {bag_rules}")

    return bag_rules


def find_contained_bags(bag_color, bag_rules):
    # Not happy with that
    nb_bags = 0

    if bag_rules[bag_color]["nb_bag_types"] > 0:

        for bc, b_nb in bag_rules[bag_color]["contains"].items():
            c_nb = find_contained_bags(bc, bag_rules)
            tmp_nb = b_nb + b_nb * c_nb
            nb_bags += tmp_nb
            logger.info(
                f"{b_nb} {bc} bag(s) adding: {b_nb} + {b_nb} * {c_nb} => {tmp_nb}. nb_bags={nb_bags}"
            )

    logger.info(f"{bag_color} contains {nb_bags}")

    return nb_bags


if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARNING)
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)

    rules = parse_bag_rules()

    searched_bag = "shiny gold"

    nb_bags = find_contained_bags(searched_bag, rules)

    print(f"{searched_bag} contains {nb_bags} bags.")
