import copy
import sys
from functools import partial
from typing import List

from utils.io import read_input_list


class WaitingArea:

    def __init__(self, inputs: List[str], task: str):
        self.cur_layout = self._parse_input(inputs)
        self.task = task
        
        self.size_i = len(self.cur_layout)
        self.size_j = len(self.cur_layout[0])
        self.deltas = {-1, 0 , 1}

        self.mutate_fn = {
            'L': self._mutate_empty,
            '#': partial(self._mutate_occupied, thresh=4 if self.task =='part-one' else 5)
        }

    def _parse_input(self, inputs: List[str]) -> List[List[str]]:
        return [list(row) for row in inputs]

    def run_process_until_stable(self):
        
        while True:
            next_layout = self._get_next_layout()
            if next_layout == self.cur_layout:
                break

            self.cur_layout = next_layout

    def get_occupied_count(self) -> int:
        total_occupied = 0
        for i in range(self.size_i):
            for j in range(self.size_j):
                if self.cur_layout[i][j] == '#':
                    total_occupied += 1

        return total_occupied

    def _get_next_layout(self) -> List[List[str]]:
        next_layout = copy.deepcopy(self.cur_layout)
        for i in range(self.size_i):
            for j in range(self.size_j):
                if next_layout[i][j] in {'#', 'L'}:
                    n_occ_adj = self._get_occ_adj_seats(i, j) if self.task == 'part-one' else self._get_occ_visable_seats(i, j)
                    next_layout[i][j] = self.mutate_fn[next_layout[i][j]](n_occ_adj)
        
        return next_layout
    
    def _get_occ_adj_seats(self, i: int, j: int) -> int:
        adj_seats = [self.cur_layout[i + i_delta][j + j_delta] 
                     for i_delta in self.deltas for j_delta in self.deltas
                     if 0 <= (i + i_delta) < self.size_i
                     and 0 <= (j + j_delta) < self.size_j
                     and not (i_delta == 0 and j_delta == 0)]
        
        return sum([1 if seat == '#' else 0 for seat in adj_seats])

    def _get_occ_visable_seats(self, i: int, j: int) -> int:
        visable_seats = []
        deltas = [(i_delta, j_delta) 
                  for i_delta in self.deltas for j_delta in self.deltas
                  if not (i_delta == 0 and j_delta == 0)]

        for i_delta, j_delta in deltas: 
            cur_i, cur_j = i + i_delta, j + j_delta 
            while 0 <= (cur_i) < self.size_i and \
                0 <= (cur_j) < self.size_j:
                    cur_visable_seat = self.cur_layout[cur_i][cur_j]
                    if cur_visable_seat != '.':
                        visable_seats.append(cur_visable_seat)
                        break

                    cur_i, cur_j = cur_i + i_delta, cur_j + j_delta
        
        return sum([1 if seat == '#' else 0 for seat in visable_seats]) 

    def _mutate_empty(self, n_occ_adj: int) -> str:
        if n_occ_adj == 0:
            return '#'
        else:
            return 'L'

    def _mutate_occupied(self, n_occ_adj: int, thresh: int) -> str:
        if n_occ_adj >= thresh:
            return 'L'
        else:
            return '#'


def part_one(input_file: str, task: str) -> int:
    # read input file
    inputs = read_input_list(input_file, strip_new_line=True)

    #instantiate WaitingArea object and run until stable
    waiting_area = WaitingArea(inputs=inputs, task=task)
    waiting_area.run_process_until_stable()

    return waiting_area.get_occupied_count()


def part_two(input_file: str, task: str) -> int:
    # read input file
    inputs = read_input_list(input_file, strip_new_line=True)

    #instantiate WaitingArea object and run until stable
    waiting_area = WaitingArea(inputs=inputs, task=task)
    
    waiting_area.run_process_until_stable()

    return waiting_area.get_occupied_count()
    

def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/11.txt', task=task)
    elif task == 'part-two':
        result = part_two(input_file='inputs/11.txt', task=task)
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
