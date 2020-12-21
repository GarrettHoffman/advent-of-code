import sys
import itertools
import re
from dataclasses import dataclass
from typing import Dict
from typing import List

from utils.io import read_input_blob


@dataclass
class Instruction:
    mem_loc: int
    value: int


@dataclass
class MaskedInstructionSet:
    mask: str
    instructions: List[Instruction]

    def run_value_masked_instructions(self, memory: Dict[int, int]):
        for instr in self.instructions:
            masked_val = self.apply_value_mask(instr.value)
            memory[instr.mem_loc] = masked_val

    def run_address_masked_instructions(self, memory: Dict[int, int]):
        for instr in self.instructions:
            masked_addresses = self.apply_address_mask(instr.mem_loc)
            for masked_adr in masked_addresses:
                memory[masked_adr] = instr.value

    def apply_value_mask(self, value: int) -> int:
        val_bin = bin(value)[2:].zfill(len(self.mask))
        
        for i, bit in enumerate(self.mask):
            if bit != 'X':
                val_bin = val_bin[:i] + bit + val_bin[i+1:]
        
        masked_val = int(val_bin, base=2)
        return masked_val

    def apply_address_mask(self, mem_loc: int) -> List[int]:
        adr_bin = bin(mem_loc)[2:].zfill(len(self.mask))
        
        for i, bit in enumerate(self.mask):
            if bit != '0':
                adr_bin = adr_bin[:i] + bit + adr_bin[i+1:]

        num_floating = adr_bin.count('X')
        bit_combinations = itertools.product(*[range(2)] * num_floating)

        masked_addresses = []
        for bit_combo in bit_combinations:
            float_adr = adr_bin
            adr_idx = 0
            float_idx = 0
            while adr_idx < len(adr_bin):
                if adr_bin[adr_idx] == 'X':
                    float_adr = float_adr[:adr_idx] + str(bit_combo[float_idx]) + float_adr[adr_idx+1:]
                    float_idx += 1

                adr_idx +=1
            
            masked_adr = int(float_adr, base=2)
            masked_addresses.append(masked_adr)
        
        return masked_addresses

    @classmethod
    def from_input_str(cls, input_str :str):
        mask, raw_instr_str = input_str[:36], input_str[36:]
        raw_instrs = [raw_instr for raw_instr in raw_instr_str.split('\n') if raw_instr]
        instructions = []
        for mem_loc, value in (re.findall(r'\d+', raw_instr) for raw_instr in raw_instrs):
            instr = Instruction(mem_loc=int(mem_loc), value=int(value))
            instructions.append(instr)

        return cls(mask, instructions)
        

class ComputerSystem:

    def __init__(self):
        self.memory = dict()

    def run_value_masked_instruction_set(self, instruction_sets: List[MaskedInstructionSet]):
        for masked_instr_set in instruction_sets:
            masked_instr_set.run_value_masked_instructions(self.memory)

    def run_address_masked_instruction_set(self, instruction_sets: List[MaskedInstructionSet]):
        for masked_instr_set in instruction_sets:
            masked_instr_set.run_address_masked_instructions(self.memory)

    def get_sum_of_mem_vals(self):
        return sum(self.memory.values())


def part_one(input_file: str) -> int:
    # read input file as blob
    input_str = read_input_blob(input_file)

    # split by mask and relevant mask instr, parse into masked instruction set objects
    mask_split = input_str.split('mask = ')[1:]
    masked_instr_sets = [MaskedInstructionSet.from_input_str(input_str) for input_str in mask_split]

    # instantiate computer system and run instruction sets
    computer = ComputerSystem()
    computer.run_value_masked_instruction_set(instruction_sets=masked_instr_sets)

    return computer.get_sum_of_mem_vals()


def part_two(input_file: str) -> int:
    # read input file as blob
    input_str = read_input_blob(input_file)

    # split by mask and relevant mask instr, parse into masked instruction set objects
    mask_split = input_str.split('mask = ')[1:]
    masked_instr_sets = [MaskedInstructionSet.from_input_str(input_str) for input_str in mask_split]

    # instantiate computer system and run instruction sets
    computer = ComputerSystem()
    computer.run_address_masked_instruction_set(instruction_sets=masked_instr_sets)

    return computer.get_sum_of_mem_vals()

    
def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/14.txt')
    elif task == 'part-two':
        result = part_two(input_file='inputs/14.txt')
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()