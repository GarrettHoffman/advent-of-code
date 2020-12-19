import sys
from dataclasses import dataclass
from functools import reduce
from typing import List
from typing import Tuple

from utils.io import read_input_list

@dataclass
class Area:

    def __init__(self, map: List[List[str]], slope: Tuple[int, int], x: int = 0, y: int = 0):
        self.map = map
        self.slope = slope
        self.x = x
        self.y = y

        self.width = len(map[0])
        self.length = len(map)

    def move(self):
        self.x = (self.x + self.slope[0]) % self.width
        self.y += self.slope[1]

    @property
    def is_on_tree(self):
        return self.map[self.y][self.x] == '#'

    @property
    def reached_bottom(self):
        return self.y >= self.length


def part_one(input_file: str, slope: Tuple[int, int]) -> int:
    # read input file
    inputs = read_input_list(input_file)

    # parse rows into cols and instantiate area
    input_map = [list(line.strip('\n')) for line in inputs]
    area = Area(map=input_map, slope=slope)
    
    # traverse area until we get to the bottom and count trees along
    # the way
    total_trees = 0
    while True:
        area.move()
        if area.reached_bottom:
            break
        
        if area.is_on_tree:
            total_trees += 1

    return total_trees


def part_two(input_file: str, slopes: List[Tuple[int, int]]) -> int:
    # iterate over slopes and run part one to get results
    results = []
    for slope in slopes:
        result = part_one(input_file=input_file, slope=slope)
        results.append(result)

    # multiple results to get final result
    result = reduce(lambda a,b: a * b, results)
    return result


def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/03.txt', slope=(3, 1))
    elif task == 'part-two':
        slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        result = part_two(input_file='inputs/03.txt', slopes=slopes)
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
