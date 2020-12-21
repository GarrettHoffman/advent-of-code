import copy
import sys
from dataclasses import dataclass
from typing import List

from utils.io import read_input_list

@dataclass
class Instruction:
    operation: str
    argument: int


class Program:

    def __init__(self, instructions: List[Instruction]):
        self.instructions = instructions
        self.accumulator = 0
        self.cur_instr_idx = 0

        self.instr_already_run = [False for _ in range(len(self.instructions))]

        self.op_fns = {
            'nop': self._nop,
            'acc': self._acc,
            'jmp': self._jmp
        }

    def run_until_loop_detected_or_completion(self):
        
        while True:
            
            # if we have terminated or have identified that we are in a loop (already
            # ran the current instruction) then we can return
            if self.is_terminated or self.instr_already_run[self.cur_instr_idx]:
                return

            # indicate that we've seen the instruction
            self.instr_already_run[self.cur_instr_idx] = True

            # run the current instruction
            cur_instr = self.instructions[self.cur_instr_idx]
            self.op_fns[cur_instr.operation](cur_instr.argument)

    def _nop(self, arg):
        self.cur_instr_idx += 1

    def _acc(self, arg):
        self.accumulator += arg
        self.cur_instr_idx += 1

    def _jmp(self, arg):
        self.cur_instr_idx += arg

    @property
    def is_terminated(self):
        return self.cur_instr_idx == len(self.instructions)


def part_one(input_file: str) -> int:
    # read input file
    inputs = read_input_list(input_file, strip_new_line=True)

    # parse inputs into instructions
    instructions = [Instruction(line.split(' ')[0], int(line.split(' ')[1])) for line in inputs]

    # instantiate the program and run until we detect a loop
    program = Program(instructions)
    program.run_until_loop_detected_or_completion()

    #return the value of the accumulator
    return program.accumulator


def part_two(input_file: str) -> int:
    # read input file
    inputs = read_input_list(input_file, strip_new_line=True)

    # parse inputs into instructions
    original_instructions = [Instruction(line.split(' ')[0], int(line.split(' ')[1])) for line in inputs]

    # find all of the nop, or jump instruction indexes instructions idx
    corruptions_candidate_fixes = []
    for i, instr in enumerate(original_instructions):
        if instr.operation == 'nop':
            corruptions_candidate_fixes.append((i, 'jmp'))

        if instr.operation == 'jmp':
            corruptions_candidate_fixes.append((i, 'nop'))

    # iterate through the candidate fixes, create a fixed instruction set, try to run and if
    # we terminate then we found the fix and can return the accumulator
    for i, new_op in corruptions_candidate_fixes:
        
        # create deep copy of original instructions
        new_instructions = copy.deepcopy(original_instructions)
        
        # fix current candidate instruction
        new_instructions[i].operation = new_op

        program = Program(new_instructions)
        program.run_until_loop_detected_or_completion()

        if program.is_terminated:
            return program.accumulator
    

def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/08.txt')
    elif task == 'part-two':
        result = part_two(input_file='inputs/08.txt')
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
