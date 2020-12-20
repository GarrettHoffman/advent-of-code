import copy
import sys
from collections import Counter
from typing import List

from utils.io import read_input_list


def part_one(input_file: str) -> int:
    # read input file
    inputs = read_input_list(input_file, line_type=int)

    # sort inputs to get adapters in order adding outlet and computer in as well
    adapters = [0] + sorted(inputs) + [max(inputs) + 3]

    # we know we have to use min joltage jump we will have to use all of our adapters
    # so we can just take the difs of all out adapters
    differences = Counter([cur - prev for (prev, cur) in zip(adapters, adapters[1:])])
    
    return differences[1] * differences[3]


def part_two(input_file: str) -> int:
    # read input file
    inputs = read_input_list(input_file, line_type=int)

    # sort inputs to get adapters in order adding outlet and computer in as well
    adapters = [0] + sorted(inputs) + [max(inputs) + 3]
    
    # we have too many branches to brute force so we need to use dynamic programming
    # let paths[i] be the total number of paths that end adapter i. 
    # We know that we can use adapters where there is a voltage difference of 1, 2 or 3
    # therefore paths[i] is paths[i-3] + paths[i-2] + paths[i-1]
    paths = [0 for _ in range(adapters[-1])]

    # fill in the base case, there is one way to have joltage 0
    paths = [1] + paths

    for adapter in adapters[1:]:
        for dif in range(1, 4):
            if adapter - dif >= 0:
                paths[adapter] += paths[adapter - dif]

    return paths[-1]
        

def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/10.txt')
    elif task == 'part-two':
        result = part_two(input_file='inputs/10.txt')
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()