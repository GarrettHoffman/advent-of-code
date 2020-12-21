import math
import sys
from typing import List

from utils.io import read_input_blob


def part_one(input_file: str):
    # read and parse input file
    inputs = read_input_blob(input_file)
    raw_earliest_time, raw_potential_buses = inputs.split('\n')

    # process inputs
    earliest_time = int(raw_earliest_time)
    potential_buses = [int(bus) for bus in raw_potential_buses.replace(',x', '').split(',')]

    # for each bus get the closest time the bus departs from our earliest time and track min
    min_wait_bus_id = 0
    min_wait_time = float('inf')
    for bus in potential_buses:
        wait_time =  math.ceil(earliest_time / bus) * bus - earliest_time
        if wait_time < min_wait_time:
            min_wait_time = wait_time
            min_wait_bus_id = bus

    return min_wait_bus_id * min_wait_time


def part_two(input_file: str):
    raise NotImplementedError
    

def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/13.txt')
    elif task == 'part-two':
        result = part_two(input_file='inputs/13.txt')
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()