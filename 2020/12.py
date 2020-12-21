import sys
from dataclasses import dataclass
from typing import List

from utils.io import read_input_list

@dataclass
class Instruction:
    action: str
    value: int


class Waypoint:

    def  __init__(self, init_y: int, init_x: int):
        self.y = init_y
        self.x = init_x

    def handle_n(self, val: int):
        self.y += val

    def handle_s(self, val: int):
        self.y -= val

    def handle_e(self, val: int):
        self.x += val

    def handle_w(self, val: int):
        self.x -= val

    def handle_l(self, val: int):
        if val == 90:
            self.x, self.y = -self.y, self.x

        if val == 180:
            self.x, self.y = -self.x, -self.y
        
        if val == 270:
            self.x, self.y = self.y, -self.x

    def handle_r(self, val: int):
        if val == 90:
            self.x, self.y = self.y, -self.x

        if val == 180:
            self.x, self.y = -self.x, -self.y
        
        if val == 270:
            self.x, self.y = -self.y, self.x
 

class Boat:

    def __init__(self, instructions: List[Instruction]):
        self.instructions = instructions
        self.waypoint = Waypoint(init_x=10, init_y=1)
        
        self.dirs = ['E', 'S', 'W', 'N']
        self.cur_dir_idx = 0
        
        self.x = 0
        self.y = 0

        self.basic_instr_fn = {
            'N': self._handle_n_basic,
            'S': self._handle_s_basic,
            'E': self._handle_e_basic,
            'W': self._handle_w_basic,
            'L': self._handle_l_basic, 
            'R': self._handle_r_basic,
            'F': self._handle_f_basic
        }

        self.waypoint_instr_fn = {
            'N': self.waypoint.handle_n,
            'S': self.waypoint.handle_s,
            'E': self.waypoint.handle_e,
            'W': self.waypoint.handle_w,
            'L': self.waypoint.handle_l, 
            'R': self.waypoint.handle_r,
            'F': self._handle_f_waypoint
        }

    def naviagate_basic(self):
        for instr in self.instructions:
            self.basic_instr_fn[instr.action](instr.value)
    
    def naviagate_waypoint(self):
        for instr in self.instructions:
            self.waypoint_instr_fn[instr.action](instr.value)

    def get_manhatten_dist(self):
        return abs(self.x) + abs(self.y)

    def _handle_n_basic(self, val: int):
        self.y += val

    def _handle_s_basic(self, val: int):
        self.y -= val

    def _handle_e_basic(self, val: int):
        self.x += val

    def _handle_w_basic(self, val: int):
        self.x -= val

    def _handle_l_basic(self, val: int):
        self.cur_dir_idx = (self.cur_dir_idx + (4 - int(val / 90))) % 4

    def _handle_r_basic(self, val: int):
        self.cur_dir_idx = (self.cur_dir_idx + int(val / 90)) % 4

    def _handle_f_basic(self, val: int):
        self.basic_instr_fn[self.dirs[self.cur_dir_idx]](val)

    def _handle_f_waypoint(self, val: int):
        self.x += val * self.waypoint.x
        self.y += val * self.waypoint.y

def part_one(input_file: str) -> int:
    # read input fil
    inputs = read_input_list(input_file, strip_new_line=True)

    # parse into instructions and instantiate boat
    instructions = [Instruction(instr[0], int(instr[1:])) for instr in inputs]
    boat = Boat(instructions=instructions)

    # navigate and return final distance
    boat.naviagate_basic()

    return boat.get_manhatten_dist()

def part_two(input_file: str) -> int:
    # read input fil
    inputs = read_input_list(input_file, strip_new_line=True)

    # parse into instructions and instantiate boat
    instructions = [Instruction(instr[0], int(instr[1:])) for instr in inputs]
    boat = Boat(instructions=instructions)

    # navigate and return final distance
    boat.naviagate_waypoint()

    return boat.get_manhatten_dist()

def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/12.txt')
    elif task == 'part-two':
        result = part_two(input_file='inputs/12.txt')
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
