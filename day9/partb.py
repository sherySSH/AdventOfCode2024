import os
from typing import List
from dataclasses import dataclass
from copy import deepcopy

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


def calc_checksum(frag_mem : List[Block]) -> int:
    checksum = 0
    # index of occupied block, if block is free space then do not update the index
    index = 0
    for block in frag_mem:
        if block.file_id != '.':
            checksum += index * int(block.file_id)
        index += 1

    return checksum


def move_files(sparse_format : List[Block]) -> list:
    head = 0
    
    tail = len(sparse_format) - 1


    # find the last file id
    while sparse_format[tail] == '.':
        tail -= 1
    
    file_id = sparse_format[tail].file_id

    while file_id != 0:

        head_offset = 0
        tail_offset = 0

        # move head to the available free space
        while head < len(sparse_format) and sparse_format[head].file_id != '.':
            head += 1

        # calculate the head offset starting from head index
        while (head + head_offset + 1) < len(sparse_format) and sparse_format[head + head_offset + 1].file_id == '.':
            head_offset += 1

        # move tail to the occupied block
        while sparse_format[tail].file_id != file_id:
            tail -= 1

        # calculate the tail offset starting from tail index
        while (tail - tail_offset - 1) >=0 and sparse_format[tail - tail_offset - 1].file_id == file_id:
            tail_offset += 1


        # once we have correct head and tail then perform swap whole file 
        # if available free space can compensate (when tail offset is less or equal to head offset) 
        # whole file otherwise we do swap file
        if tail_offset <= head_offset and head < tail:
           # swap all blocks of a file
            for offset in range(tail_offset + 1):
                # swap block
                temp = sparse_format[tail - offset]
                sparse_format[tail - offset] = Block(file_id='.')
                sparse_format[head + offset] = temp
        
            file_id = file_id - 1
            # move head back to the original position after successful swap
            head = 0

        else:
            # head would move if current file does not fit in the free space to find next chunk of free space
            head = head + head_offset + 1
        
            # switch to lower file id if current file cannot be moved to any free space on the left side
            if head >= tail:
                file_id = file_id - 1
                # move head back to the original position after trying all free space blocks
                head = 0
                # move tail as well since attempt to move file failed
                tail = tail - tail_offset - 1
        

    return sparse_format


if __name__ == "__main__":
    disk_map = read_file('input.txt')
    sparse_format = uncompress(disk_map)

    moved_mem = move_files(sparse_format)
    checksum = calc_checksum(moved_mem)
    print("Part b:", checksum)