from typing import List

def read_file(path : str):
    with open(path, 'r') as f:
        content = f.read()
    return content

def processing(content : str):
    stones = content.split(" ")
    stones = [int(stone) for stone in stones]
    return stones

def calc_n_stones(n_blinks : int):
    for index, _ in enumerate(stones):
        if stones[index] == 0:
            pass
        
        elif len(str(stones[index])) % 2 == 0:
            pass

        else:
            pass

        
if __name__ == "__main__":
    content = read_file("input.txt")
    stones = processing(content)
    print(stones)