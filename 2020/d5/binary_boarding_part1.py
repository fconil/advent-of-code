"""
@author: fconil
https://adventofcode.com/2020/day/5

Day 5: Binary Boarding
"""
import logging

logger = logging.getLogger(__name__)


def get_range(letter, seat_range):
    count = seat_range.stop - seat_range.start

    logger.debug(f"count={count}")

    result = None

    if count == 2:
        # F: Front : lower half
        # L: Left:  lower half
        if letter in ("F", "L"):
            result = seat_range.start

        # B: Back: upper half
        # R: Right: upper half
        if letter in ("B", "R"):
            result = seat_range.stop - 1
    else:
        middle = count // 2

        # F: Front : lower half
        # L: Left:  lower half
        if letter in ("F", "L"):
            result = range(seat_range.start, seat_range.start + middle)

        # B: Back: upper half
        # R: Right: upper half
        if letter in ("B", "R"):
            result = range(seat_range.start + middle, seat_range.stop)

    if isinstance(result, int):
        logger.debug(f"{letter} => final row {result}")
    else:
        logger.debug(f"{letter} => {result.start} .. {result.stop}")

    return result


def get_element(filter, size):
    logger.info(f"Find element in {size} elements with filter={filter}")

    current_range = range(size)
    logger.debug(f"starting => {current_range.start} .. {current_range.stop -1 } ")

    for l in filter:
        if isinstance(current_range, range):
            current_range = get_range(l, current_range)

    return current_range


def get_seat(seat_filter):
    row = get_element(seat_filter[:7], 128)
    col = get_element(seat_filter[-3:], 8)

    seat_id = (row * 8) + col

    logger.info(
        f"Filter: {seat_filter}, seat row: {row}, seat col: {col}, "
        f"seat ID:{seat_id}"
    )

    return seat_id


if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARNING)
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)

    seat_id_list = []

    with open("input", "r") as f:
        l_input = [l.rstrip("\n") for l in f.readlines()]  # noqa E741

    for filter in l_input:
        seat_id = get_seat(filter)

        seat_id_list.append(seat_id)

    print(f"Highest seat ID = {max(seat_id_list)}")
