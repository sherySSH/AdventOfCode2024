import os
from typing import List
from dataclasses import dataclass

@dataclass
class Block:
    file_id : str

def read_file(path : str) -> str:
    with open(path, 'r') as f:
        content = f.read()
    return content


def uncompress(disk_map : str):
    mode = 'file'
    file_id = -1
    sparse_format = []
    
    for n_blocks in disk_map:
        
        if mode == 'file':
            file_id += 1
            block = Block(file_id=file_id)
            mode = 'free'
        elif mode == 'free':
            block = Block(file_id='.')
            mode = 'file'

        for _ in range(int(n_blocks)):
            sparse_format.append(block)

    return sparse_format

def fragment(sparse_format : List[Block]) -> list:
    head = 0
    tail = len(sparse_format) - 1
    while head < tail:
        
        # move head to the available free space
        while sparse_format[head].file_id != '.':
            head += 1

        # move tail to the occupied bloack
        while sparse_format[tail].file_id == '.':
            tail -= 1
        
        if head > tail:
            break

        # once we have correct head and tail then perform swap
        temp = sparse_format[tail]
        sparse_format[tail] = Block(file_id='.')
        sparse_format[head] = temp

    return sparse_format


def calc_checksum(frag_mem : List[Block]) -> int:
    checksum = 0
    # index of occupied block, if block is free space then do not update the index
    index = 0
    for block in frag_mem:
        if block.file_id != '.':
            checksum += index * int(block.file_id)
        index += 1

    return checksum



if __name__ == "__main__":
    disk_map = read_file('input.txt')
    sparse_format = uncompress(disk_map)
    
    frag_mem = fragment(sparse_format)
    checksum = calc_checksum(frag_mem)
    print("Part a:", checksum)
