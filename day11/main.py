from typing import List, Mapping
import math
from collections import Counter
from dataclasses import dataclass

@dataclass
class CachedStone:
    split_stones : list
    blink_count : int

def read_file(path : str):
    with open(path, 'r') as f:
        content = f.read()
    return content

def processing(content : str) -> List[int]:
    stones = content.split(" ")
    stones = [int(stone) for stone in stones]
    return stones

def get_blink_from_table(stone : int, remaining_blinks : int, table : Mapping[int, Mapping[int, List[int]]]):
    possible_blinks : list = list(table[stone].keys())
    blink = possible_blinks.pop()
    while blink > remaining_blinks:
        if len(possible_blinks) != 0:
            blink = possible_blinks.pop()
        else:
            blink = 1
    # print(blink, remaining_blinks)
    return blink

def calc_n_stones(blink_count : int, n_blinks : int, stones : list):
    
    # base case
    if blink_count > n_blinks:
        return stones
    # recursive case
    else:
        split_stones = []
        for index, _ in enumerate(stones):
            if stones[index] == 0:
                split_stones.append(1)
            
            elif len(str(stones[index])) % 2 == 0:
                start = 0
                end = len(str(stones[index]))
                half = (start + end ) // 2
                
                split_stones.append( int(str(stones[index])[start:half]) )
                
                split_stones.append( int(str(stones[index])[half:end]) )

            else:
                split_stones.append( stones[index] * 2024 )
        
        blink_count += 1
        return calc_n_stones(blink_count, n_blinks, split_stones)


def splitted(stone : int):
        if stone == 0:
            return [1]
        # if number of digits are even
        elif len(str(stone)) % 2 == 0:
            start = 0
            end = len(str(stone))
            half = (start + end ) // 2
            return [ int(str(stone)[start:half]) , int(str(stone)[half:end]) ]

        else:
            return [stone * 2024]


def calc_n_stones_compressed(n_blinks, stones : dict, blink_count : int = 0):

    """
    We are using BFS traversal for stone splitting. This means we move onto next level
    for recursively splitting the stones, once we have splitted all stones at current level.
    Storing individual stones is expensive due to huge memory footprint, therefre I compress
    them by just storing the counts of a stone. So if at a given level, if a stone "4" occurs
    10 times then 4 would be a key and 10 would be its value. This is a memory efficient way
    of storing stones intead of storing them individually.
    """
    
    if blink_count == n_blinks:
        return sum(stones.values())
    # new level of stones
    new_stones = {}
  
    for stone, freq in stones.items():
        
        for new_stone in splitted(stone):
            # storing number of splitted stones for a current stones 
            
            if new_stone not in new_stones:
                new_stones[new_stone] = freq
            else:
                new_stones[new_stone] += freq

    blink_count += 1

    return calc_n_stones_compressed(n_blinks, new_stones, blink_count)


if __name__ == "__main__":
    content = read_file("input.txt")
    stones : List[int] = processing(content)
    split_stones = calc_n_stones(1, 25, stones)
    print("Part a:", len(split_stones))

    n_stones = calc_n_stones_compressed(n_blinks=75, stones = Counter(stones), blink_count= 0)
    print("Part b:", n_stones)

   