import typing
import copy

class Instruction:

    def __init__(self, opcode: int, arg_addresses: [int], res_address: int, intcode_program_memory: [int]):
        self.opcode = opcode
        self.arg_addresses = arg_addresses
        self.res_address = res_address

        self.intcode_program_memory = intcode_program_memory

        self.opcode_map = {
            1: self.add,
            2: self.multiply,
            99: self.terminate
        }

    def add(self) -> (str, [int]):
        res = self.intcode_program_memory[self.arg_addresses[0]] + self.intcode_program_memory[self.arg_addresses[1]]
        self.intcode_program_memory[self.res_address] = res
        return 'ADDED', self.intcode_program_memory

    def multiply(self) -> (str, [int]):
        res = self.intcode_program_memory[self.arg_addresses[0]] * self.intcode_program_memory[self.arg_addresses[1]]
        self.intcode_program_memory[self.res_address] = res
        return 'MULTIPLIED', self.intcode_program_memory

    def terminate(self) -> (str, [int]):
        return 'TERMINATED', self.intcode_program_memory

    def execute(self) -> (str, [int]):
        res, intcode_program_stage = self.opcode_map[self.opcode]()
        return res, intcode_program_stage

class IntcodeComputer:

    def __init__(self, intcode_program_file: str):
        
        self.intcode_program = self.read_incode_input_file(intcode_program_file)

    def read_incode_input_file(self, intcode_input_file: str) -> [int]:
        input_str = None
        with open(intcode_input_file) as f:
            input_str = f.read()

        input_list = [int(num) for num in input_str.split(",")]
        return input_list

    def run_program(self, noun: int, verb: int) -> int:
        intcode_program_memory = copy.deepcopy(self.intcode_program)
        intcode_program_memory[1] = noun
        intcode_program_memory[2] = verb

        for i in range(0, len(intcode_program_memory), 4):
            instruction = self.parse_instruction(i, intcode_program_memory)
            res, intcode_program_memory = instruction.execute()
            if res == 'TERMINATED':
                break
        
        result = intcode_program_memory[0] 
        return result

    def parse_instruction(self, i: int, intcode_program_memory: [int]) -> Instruction:
        opcode, *arg_addresses, res_address = intcode_program_memory[i:i+4]
        instruction = Instruction(opcode, arg_addresses, res_address, intcode_program_memory)
        return instruction

    def run_input_search(self, range_min: int, range_max: int, search_result: int) -> (int, int):
        for noun in range(range_min, range_max + 1):
            for verb in range(range_min, range_max + 1):
                solution_found = False
                try:
                    result = self.run_program(noun, verb)
                except IndexError:
                    continue

                if result == search_result:
                    solution_found = True
                    break

            if solution_found:
                break
        return noun, verb

if __name__ == '__main__':
    intcode_computer = IntcodeComputer('input.txt')
    part_one_solution = intcode_computer.run_program(12, 2)
    print("The value in res_address 0 for part 1 is: ", part_one_solution)
    noun, verb = intcode_computer.run_input_search(0, 99, 19690720)
    part_two_solution = 100 * noun + verb
    print(f"The value of the noun and verb for program value {19690720} are {noun} and {verb}, and the solution is {part_two_solution}")