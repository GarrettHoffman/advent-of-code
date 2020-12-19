import sys


def main():
    try:
        _, task = sys.argv
    except ValueError:
        task = None

    if task == 'part-one':
        result = part_one(input_file='inputs/03.txt', slope=(3, 1))
    # elif task == 'part-two':
    #     slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    #     result = part_two(input_file='inputs/03.txt', slopes=slopes)
    else:
        print(f"Must specify 'part-one' or 'part-two'. Usage: python {__file__} [part-one OR part-two]")
        return
    
    print("Result:", result)


if __name__ == "__main__":
    main()
