import sys
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional

from utils.io import read_input_list

@dataclass
class InnerBag:
    color: str
    amount: int


def part_one(input_file: str, desired_bag_color: str) -> int:
    # read input file
    inputs = read_input_list(input_file, strip_new_line=True)

    # parse our rules and create a mapping of bags > inner bags
    bag_tree = {}
    for line in inputs:
        raw_bag_color, raw_inner_bags = line.split('contain')
        
        bag_color = "_".join(raw_bag_color.replace('bags', '').strip().split())
        inner_bags = process_raw_inner_bags(raw_inner_bags)
        bag_tree[bag_color] = inner_bags

    # initialize container for valid outer colors and do a breadth first search
    # starting at each outer color and see if we find the desired color

    bags_containing_desired_color = set()

    def breadth_first_search(initial_color: str, desired_color: str) -> None:
        queue = [inner_bag.color for inner_bag in bag_tree.get(initial_color, [])]

        while queue:

            current_bag_color = queue.pop()

            if current_bag_color == desired_color:
                bags_containing_desired_color.add(initial_color)
                return

            inner_bags = bag_tree.get(current_bag_color, [])
            for inner_bag in inner_bags:
                queue.append(inner_bag.color)

    for initial_color in bag_tree:
        breadth_first_search(initial_color, desired_bag_color)

    return len(bags_containing_desired_color)


def part_two(input_file: str, desired_bag_color: str) -> int:
    # read input file
    inputs = read_input_list(input_file, strip_new_line=True)

    # parse our rules and create a mapping of bags > inner bags
    bag_tree = {}
    for line in inputs:
        raw_bag_color, raw_inner_bags = line.split('contain')
        
        bag_color = "_".join(raw_bag_color.replace('bags', '').strip().split())
        inner_bags = process_raw_inner_bags(raw_inner_bags)
        bag_tree[bag_color] = inner_bags

    def breadth_first_search(initial_color: str, total_bags) -> None:
        # initialize queue of tupples of bags to count along with the number of 
        # "parent bags" to multiply our the quantities
        queue = [(inner_bag, 1) for inner_bag in bag_tree.get(initial_color, [])]

        while queue:

            # pop off next bag with parent count and add the number of this bag to the
            # total
            current_bag, parent_count = queue.pop()
            total_bags += current_bag.amount * parent_count

            # iterate over the inner bags of the current bag and add to queue with new
            # parent count
            for inner_bag in bag_tree.get(current_bag.color, []):
                queue.append((inner_bag, parent_count * current_bag.amount))
        
        return total_bags

    total_bags = breadth_first_search(desired_bag_color, 0)

    return total_bags

        
def process_raw_inner_bags(raw_inner_bags: str) -> List[Optional[InnerBag]]:
    # parse raw inner bags string
    split_inner_bags = [item.replace('bags', '').replace('bag', '').strip('.').strip() for item in raw_inner_bags.split(",")]

    # handle case where we have no inner bags
    if split_inner_bags == ['no other']:
        return []

    inner_bags = []
    for raw_inner_bag in split_inner_bags:
        raw_amount, *raw_color = raw_inner_bag.split(' ')
        
        amount = int(raw_amount)
        color = '_'.join(raw_color)

        inner_bags.append(InnerBag(color, amount))
    
    return inner_bags
            

def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/07.txt', desired_bag_color='shiny_gold')
    elif task == 'part-two':
        result = part_two(input_file='inputs/07.txt', desired_bag_color='shiny_gold')
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
