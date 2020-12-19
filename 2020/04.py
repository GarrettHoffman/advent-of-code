import re
import sys
from typing import Dict
from typing import List
from typing import Set

from utils.io import read_input_blob

class Passport():
    
    def __init__(self, data: Dict[str, str]):
        self.data = data

        self.validation_fns = {
            'byr': self._validate_byr,
            'iyr': self._validate_iyr,
            'eyr': self._validate_eyr,
            'hgt': self._validate_hgt,
            'hcl': self._validate_hcl,
            'ecl': self._validate_ecl,
            'pid': self._validate_pid,
            'cid': lambda: True
        }
    
    @classmethod
    def from_input_str(cls, input_str:str):
        key_val_pairs = [pair.split(':') for pair in input_str.split(' ')]
        data = dict(key_val_pairs)
        return cls(data=data)

    def has_valid_fields(self, required_fields: Set[str]) -> bool:
        return required_fields.issubset(self.data.keys())

    @property
    def has_valid_data(self) -> bool:
        return all([self.validation_fns[key]() for key in self.data.keys()])

    def _validate_byr(self):
        byr = self.data.get('byr')
        return len(byr) == 4 and 1920 <= int(byr) <= 2002

    def _validate_iyr(self):
        iyr = self.data.get('iyr')
        return len(iyr) == 4 and 2010 <= int(iyr) <= 2020

    def _validate_eyr(self):
        eyr = self.data.get('eyr')
        return len(eyr) == 4 and 2020 <= int(eyr) <= 2030

    def _validate_hgt(self):
        hgt = self.data.get('hgt', '')
        
        units = hgt[-2:]
        value = hgt[:-2]
        
        return units in {'cm', 'in'} and self._validate_hgt_by_units(value, units)
    
    def _validate_hgt_by_units(self, value: str, units: str):
        return 150 <= int(value) <= 193 if units == 'cm' else 59 <= int(value) <= 76

    def _validate_hcl(self):
        return bool(re.fullmatch(r'#[a-f0-9]{6}', self.data.get('hcl')))

    def _validate_ecl(self):
        return self.data.get('ecl') in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

    def _validate_pid(self):
        return bool(re.fullmatch(r'\d{9}', self.data.get('pid')))


def part_one(input_file: str, required_fields: Set[str]) -> int:
    # read input file
    inputs = read_input_blob(input_file)

    # parse raw input and marshal into Passport object
    passports = []
    for line in inputs.split('\n\n'):
        passport = Passport.from_input_str(line.replace('\n', " "))
        passports.append(passport)

    # iterate through passports and count the number that are valid
    total_valid = 0
    for passport in passports:
        if passport.has_valid_fields(required_fields=required_fields):
            total_valid += 1

    return total_valid


def part_two(input_file: str, required_fields: Set[str]) -> int:
    # read input file
    inputs = read_input_blob(input_file)

    # parse raw input and marshal into Passport object
    passports = []
    for line in inputs.split('\n\n'):
        passport = Passport.from_input_str(line.replace('\n', " "))
        passports.append(passport)

    # iterate through passports and count the number that are valid
    total_valid = 0
    for passport in passports:
        if passport.has_valid_fields(required_fields=required_fields) \
                and passport.has_valid_data:
            total_valid += 1

    return total_valid


def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl' ,'ecl', 'pid'}
        result = part_one(input_file='inputs/04.txt', required_fields=required_fields)
    elif task == 'part-two':
        required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl' ,'ecl', 'pid'}
        result = part_two(input_file='inputs/04.txt', required_fields=required_fields)
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
