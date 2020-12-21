import sys
from dataclasses import dataclass

from utils.io import read_input_blob


@dataclass
class NumberData:
    times_spoken: int
    last_spoken: int
    next_to_last_spoken: int = None


def part_one(input_file: str, last_turn: int) -> int:
    # read input list
    inputs = read_input_blob(input_file)

    # part to form starting list
    starting_list = [int(num) for num in inputs.split(',')]
    
    # instantiate turn counter, last work and dict to keep track data about the number
    # that was last said
    turn = 0
    last_spoken_num = None
    
    previously_spoken = dict()

    for num in starting_list:
        turn += 1
        last_spoken_num = num
        previously_spoken[num] = NumberData(times_spoken=1, last_spoken=turn)
        
    # follow rules based on last_spoken_num until we reach our turn limit
    while turn != last_turn:
        turn += 1
        # if last spoken work was spoken for the first time then the cur num spoken
        # is 0, otherwise it is the delta between the curruent turn and the last turn
        # that the previous number was spoken
        if previously_spoken[last_spoken_num].times_spoken == 1:
            cur_num = 0
        else:
            cur_num = previously_spoken[last_spoken_num].last_spoken - previously_spoken[last_spoken_num].next_to_last_spoken

        # update the previously spoken dict with the current num
        if cur_num not in previously_spoken:
            previously_spoken[cur_num] = NumberData(times_spoken=1, last_spoken=turn)
        else:
            previously_spoken[cur_num].times_spoken += 1
            previously_spoken[cur_num].next_to_last_spoken = previously_spoken[cur_num].last_spoken
            previously_spoken[cur_num].last_spoken = turn

        last_spoken_num = cur_num

    return last_spoken_num
        

def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/15.txt', last_turn=2020)
    elif task == 'part-two':
        result = part_one(input_file='inputs/15.txt', last_turn=30000000)
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
