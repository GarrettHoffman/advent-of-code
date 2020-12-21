import math
import sys
from typing import List

from utils.io import read_input_blob


# NOT MY CODE : https://rosettacode.org/wiki/Chinese_remainder_theorem
from functools import reduce
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
#  NOT MY CODE ENDS HERE


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
    # read and parse input file
    inputs = read_input_blob(input_file)
    _, raw_buses = inputs.split('\n')

    # process inputs and get diffs for crt
    buses = [int(bus) if bus[0] != 'x' else 0 for bus in raw_buses.split(",")]
    diffs = [bus - i for i, bus in enumerate(buses)]

    # remove the 0s (formerly xs) from buses and difs
    rel_buses = []
    rel_diffs = []
    for i, bus in enumerate(buses):
        if bus > 0:
            rel_buses.append(bus)
            rel_diffs.append(diffs[i])

    return chinese_remainder(rel_buses, rel_diffs)


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
