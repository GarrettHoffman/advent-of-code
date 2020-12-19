from typing import List

def read_input_list(file: bytes, line_type: type = str) -> List[int]:
    int_list = []
    with open(file) as f:
        for line in f.readlines():
            int_list.append(line_type(line))

    return int_list
        