import sys
from typing import List

from utils.io import read_input_blob

def part_one(input_file: bytes) -> int:
    # read input file
    inputs = read_input_blob(input_file)

    # split groups and combine all group answers into a single line
    groups = []
    for line in inputs.split('\n\n'):
        groups.append(line.replace('\n', ''))

    # iterate through groups and count uniques
    total_answer_counts = 0
    for group in groups:
        total_answer_counts += len(set(group))

    return total_answer_counts


def part_two(input_file: bytes) -> int:
     # read input file
    inputs = read_input_blob(input_file)

    # split groups and then split each member for the group
    groups = []
    for line in inputs.split('\n\n'):
        group = line.split('\n')
        groups.append(group)

    # iterate through groups and get the count of questions that
    # were answered by all memebers, tracking total along the way
    total_all_yes_counts = 0
    for group in groups:
        for question in group[0]:
            if all([question in memember for memember in group]):
                total_all_yes_counts += 1

    return total_all_yes_counts


def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/06.txt')
    elif task == 'part-two':
        result = part_two(input_file='inputs/06.txt')
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()