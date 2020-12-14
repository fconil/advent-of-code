"""
@author: fconil
https://adventofcode.com/2020/day/8

Day 8: Handheld Halting
"""
import logging

logger = logging.getLogger(__name__)


def load_code():
    with open("input") as f:
        instructions = [l.rstrip("\n").split() for l in f.readlines()]  # noqa E741

    return instructions


class Processor:
    def __init__(self):
        self.accumulator = 0
        self.current_instr = 0

        self.operations = {
            "nop": self.nop,
            "acc": self.acc,
            "jmp": self.jmp,
        }

        self.executed = []

    def nop(self, no, val):
        logger.debug(f"instruction {no} - NOP")
        return no + 1

    def acc(self, no, val):
        self.accumulator += val
        logger.debug(f"instruction {no} - ACC {val} - accumulator: {self.accumulator}")
        return no + 1

    def jmp(self, no, val):
        next_instr = no + val
        logger.debug(f"instruction {no} - JMP {val} - next: {next_instr}")
        return next_instr

    def execute_instruction(self, no):
        instruction = self.instructions[no][0]
        value = int(self.instructions[no][1])
        return self.operations[instruction](no, value)

    def __call__(self, instructions):
        self.instructions = instructions

        nb_instructions = len(instructions)
        next_instr = 0

        while True:
            self.executed.append(next_instr)
            next_instr = self.execute_instruction(next_instr)

            if next_instr >= nb_instructions:
                print(
                    f"End of program - accumulator: {self.accumulator} - next: {next_instr}"
                )
                break

            if next_instr in self.executed:
                print(
                    f"Infinite loop - accumulator: {self.accumulator} - next: {next_instr}"
                )
                break


if __name__ == "__main__":
    # logging.basicConfig(level=logging.WARNING)
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)

    instructions = load_code()
    proc = Processor()
    proc(instructions)
