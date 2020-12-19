from typing import List

def read_input_list(file: bytes, line_type: type = str, strip_new_line: bool = False) -> List[int]:
    input_list = []
    with open(file) as f:
        for line in f.readlines():
            if strip_new_line:
                line = line.replace('\n', '')
            input_list.append(line_type(line))

    return input_list

def read_input_blob(file: bytes) -> List[int]:
    with open(file) as f:
        return f.read()
