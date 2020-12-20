import sys
from typing import List

from utils.io import read_input_list


def is_valid(num: int, preamble: List[int]) -> bool:
    has_property = False
    
    for i, value in enumerate(preamble):
        other_value = num - value
        if other_value in preamble[i+1:]:
            has_property = True
            break

    return has_property
            

def part_one(input_file: str, preamble_len: int) -> int:
    # read input file
    inputs = read_input_list(input_file, line_type=int)

    # iterate over all values starting after the preamble and
    # check if they are valid. Return once we find the first invalid
    for i, num in enumerate(inputs[preamble_len:]):
        # since we are enumerating starting after the preamble the i in our
        # loop will actually be the start of the preamble (our first value is inputs[25])
        # and our i = 0, so the preamble is the slice [i, i + preamble_len]
        preamble = inputs[i: i + preamble_len]
        if not is_valid(num, preamble):
            return num


def part_two(input_file: str, preamble_len: int) -> int:
    # read input file
    inputs = read_input_list(input_file, line_type=int)

    # get target value from part one
    target = part_one(input_file, preamble_len)

    # perform a brute force search looking for the cumulative sum equal to our targe
    range_found = False
    
    for i in range(len(inputs)):
        for j in range(i+1, len(inputs)):
            if sum(inputs[i:j+1]) == target:
                range_found = True
                break

        if range_found:
            break

    minimum = min(inputs[i:j+1])
    maximum = max(inputs[i:j+1])
                
    return minimum + maximum        


def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/09.txt', preamble_len=25)
    elif task == 'part-two':
        result = part_two(input_file='inputs/09.txt', preamble_len=25)
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()