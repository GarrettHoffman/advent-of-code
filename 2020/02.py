import sys
from dataclasses import dataclass

from utils.io import read_input_list

@dataclass
class PasswordData:
    letter: str
    minimum: int
    maximum: int
    password: str
    
    @classmethod
    def from_input_str(cls, input_str: str):
        cnt_range, letter, password = input_str.split(" ")
        mininum, maximum = [int(value) for value in cnt_range.split("-")]
        letter = letter.strip(":")
        
        return cls(letter=letter, minimum=mininum, maximum=maximum, password=password)

    @property
    def is_valid_count(self):
        return self.minimum <= self.password.count(self.letter) <= self.maximum

    @property
    def is_valid_position(self):
        return (self.password[self.minimum-1] == self.letter) ^ (self.password[self.maximum-1] == self.letter)

        
def part_one(input_file: bytes) -> int:
    # read input file
    inputs = read_input_list(input_file)

    # parse inputs
    passwords = [PasswordData.from_input_str(input_str) for input_str in inputs]

    # iterate over all passwords and count if valid
    total_valid = 0
    for password in passwords:
        if password.is_valid_count:
            total_valid += 1

    return total_valid


def part_two(input_file: bytes) -> int:
    # read input file
    inputs = read_input_list(input_file)

    # parse inputs
    passwords = [PasswordData.from_input_str(input_str) for input_str in inputs]

    # iterate over all passwords and count if valid
    total_valid = 0
    for password in passwords:
        if password.is_valid_position:
            total_valid += 1

    return total_valid


def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/02.txt')
    elif task == 'part-two':
        result = part_two(input_file='inputs/02.txt')
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
