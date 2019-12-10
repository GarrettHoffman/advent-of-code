import re
import typing

class PasswordManager:

    def __init__(self, input_file: str):
        self.min, self.max = self.parse_input_file(input_file)

    def parse_input_file(self, input_file: str) -> [int, int]:
        range_str = None
        with open(input_file) as f:
            range_str = f.read()
        range_list = [int(num) for num in range_str.split("-")]
        return range_list

    def is_non_decreasing(self, candidate: int) -> bool:
        is_non_decreasing = True
        digits = [int(digit) for digit in str(candidate)]
        for i in range(1, len(digits)):
            if digits[i] < digits[i-1]:
                is_non_decreasing = False
                break
        return is_non_decreasing

    def has_at_least_one_repeating(self, candidate: int) -> bool:
        at_least_one_repeating = False
        digits = [int(digit) for digit in str(candidate)]
        for i in range(1, len(digits)):
            if digits[i] == digits[i-1]:
                at_least_one_repeating = True
                break
        return at_least_one_repeating
    
    def has_at_least_one_repeating_with_no_larger_group(self, candidate: int) -> bool:
        at_least_one_repeating_no_larger_group = False
        digits = [int(digit) for digit in str(candidate)]
        for i in range(1, len(digits)):
            if i == 1:
                if (digits[i] == digits[i-1]) and (digits[i+1] != digits[i]):
                    at_least_one_repeating_no_larger_group = True
                    break
            elif i == (len(digits) - 1):
                if (digits[i] == digits[i-1]) and (digits[i-1] != digits[i-2]):
                    at_least_one_repeating_no_larger_group = True
                    break
            else:
                if (digits[i] == digits[i-1]) and (digits[i+1] != digits[i]) and (digits[i-1] != digits[i-2]):
                    at_least_one_repeating_no_larger_group = True
                    break
        return at_least_one_repeating_no_larger_group

    def count_valid_passwords(self):
        valide_passwords = 0
        for candidate in range(self.min, self.max+1):
            if self.is_non_decreasing(candidate) and self.has_at_least_one_repeating(candidate):
                valide_passwords += 1
        return valide_passwords

    def count_valid_passwords_with_no_larger_group(self):
        valide_passwords = 0
        for candidate in range(self.min, self.max+1):
            if self.is_non_decreasing(candidate) and self.has_at_least_one_repeating_with_no_larger_group(candidate):
                valide_passwords += 1
        return valide_passwords

if __name__ == '__main__':
    password_manager = PasswordManager('input.txt')
    part_1_solution = password_manager.count_valid_passwords()
    print(f"the number of valid passwords for part 1 is {part_1_solution}")
    part_2_solution = password_manager.count_valid_passwords_with_no_larger_group()
    print(f"the number of valid passwords for part 1 is {part_2_solution}")