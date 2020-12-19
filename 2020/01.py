import sys

from utils.io import read_input_list

def part_one(input_file: str, total: int) -> int:
    # read in input file
    expenses = read_input_list(input_file, line_type=int)

    # iterate through the values and get what the other value would
    # need to be for this pair to be the solution
    for value in expenses:
        other_value = total - value
        if other_value in expenses:
            return value * other_value


def part_two(input_file: str, total: int) -> int:
    # read in input file
    expenses = read_input_list(input_file, line_type=int)

    # iterate through with indexes so we dont re-check the first pair of 
    # numbers
    for i, value in enumerate(expenses):
        for second_value in expenses[i+1:]:
            third_value = total - value - second_value
            if third_value in expenses:
                return value * second_value * third_value


def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/01.txt', total=2020)
    elif task == 'part-two':
        result = part_two(input_file='inputs/01.txt', total=2020)
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
