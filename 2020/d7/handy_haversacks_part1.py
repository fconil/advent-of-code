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

    bag_rules = []

    for line in l_input:
        logger.debug(f"Parse line: {line}")

        m = bag_rules_pattern.match(line)
        if m is not None:
            logger.debug(f"{m.groupdict()}")
            bag_rules.append(m.groupdict())
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
    for rule in bag_rules:
        rule["bag_content"] = rule["bag_content"].strip(".")
        content = [bag.strip() for bag in rule["bag_content"].split(",")]

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
    logger.debug(f"Rule list: {bag_rules}")

    return bag_rules


def find_direct_containers(bag_color, bag_rules):
    containers = set()
    for rule in bag_rules:
        if (rule["nb_bag_types"] > 0) and (bag_color in rule["contains"].keys()):
            containers.add(rule["bag_color"])

    logger.debug(containers)

    logger.info(f"{bag_color} found in {containers}")

    return containers


def find_all_containers(searched_bag, rules):
    all_containers = set()
    all_containers.add(searched_bag)

    searched_containers = find_direct_containers(searched_bag, rules)

    all_containers = all_containers.union(searched_containers)

    while len(searched_containers) > 0:
        new_containers = set()

        for searched_bag in searched_containers:
            found_containers = find_direct_containers(searched_bag, rules)

            new_containers = new_containers.union(
                found_containers.difference(searched_containers)
            )

        searched_containers = new_containers
        all_containers = all_containers.union(searched_containers)

    all_containers.remove(searched_bag)

    logger.info(f"All containers found for {searched_bag}: {all_containers}")

    return all_containers


if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARNING)
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)

    rules = parse_bag_rules()

    searched_bag = "shiny gold"

    containers = find_all_containers(searched_bag, rules)

    print(f"{searched_bag} is contained in {len(containers)} bags: {containers}")
