"""
@author: fconil
https://adventofcode.com/2020/day/6

Day 6: Custom Customs
"""
import array
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARNING)
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)

    with open("input", "r") as f:
        l_input = [l.rstrip("\n") for l in f.readlines()]  # noqa E741

    count_yes = []
    new_group = True

    for line in l_input:
        logger.debug(f"Line : {line}")
        if len(line) == 0:
            count_yes.append(group_yes)
            new_group = True
        else:
            responses = set(array.array("u", line).tolist())
            if new_group:
                group_yes = responses
                new_group = False
            else:
                group_yes &= responses

    # Last group
    count_yes.append(group_yes)

    nb_yes_per_group = [len(sgy) for sgy in count_yes]
    sum_yes = sum(nb_yes_per_group)

    logger.info(
        f"Nb groups: {len(count_yes)}, count_yes: {count_yes}, "
        f"nb yes per group: {nb_yes_per_group}"
    )

    print(f"Sum of yes answers: {sum_yes} ")
