import sys
from typing import List
from typing import Tuple

from utils.io import read_input_list

def find_seat(ticket: str, plane_size: Tuple[int, int]):
    # find row
    rows = list(range(plane_size[0]))
    row = binary_search(directions=ticket[:7], item_range=rows)
    
    # find col
    cols = list(range(plane_size[1]))
    col = binary_search(directions=ticket[-3:], item_range=cols)
    
    #return seat number
    return row * 8 + col

def binary_search(directions: str, item_range: List[int]):
    n_directions = len(directions)
    current_direction = directions[0]
    
    midpoint = int(len(item_range) / 2)
    
    # base case when down to last direction
    if n_directions == 1: 
        if current_direction in {'F', 'L'}:
            return item_range[0]
        else:
            return item_range[1]

    # otherwise call binary_search recursively on applicable half of range with the
    # remaining directions
    else:
        if current_direction in {'F', 'L'}:
            return binary_search(directions=directions[1:], item_range=item_range[:midpoint])
        else:
            return binary_search(directions=directions[1:], item_range=item_range[midpoint:])


def part_one(input_file: str, plane_size: Tuple[int, int]) -> int:
    # read input file
    inputs = read_input_list(input_file, strip_new_line=True)

    # iterate through tickets and find the seat id
    # keep track of max seat id along the way
    max_seat_id = -float('inf')
    for ticket in inputs:
        seat_id = find_seat(ticket=ticket, plane_size=plane_size)
        if seat_id > max_seat_id:
            max_seat_id = seat_id

    return max_seat_id


def part_two(input_file: str, plane_size: Tuple[int, int]) -> int:
    # read input file
    inputs = read_input_list(input_file, strip_new_line=True)

    # collect known seats
    known_seats = [find_seat(ticket=ticket, plane_size=plane_size) for ticket in inputs]

    # for each seat check if there is an empty seat on either side of the seat
    # between another known seat
    for seat in known_seats:
        if seat - 1 not in known_seats and seat - 2 in known_seats:
            return seat - 1
        
        if seat + 1 not in known_seats and seat + 2 in known_seats:
            return seat + 1
    

def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/05.txt', plane_size=(128, 8))
    elif task == 'part-two':
        result = part_two(input_file='inputs/05.txt', plane_size=(128, 8))
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
