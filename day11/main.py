from typing import List, Mapping
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

def calc_n_stones(blink_count : int, n_blinks : int, stones : list):
    print(blink_count)
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

def cache_a_stone(initial_stone : int, stones : list, table : dict, blink_count : int = 0):
    
    # base case
    if initial_stone in stones and len(stones) != 1:
        table[initial_stone] = CachedStone(split_stones=stones, blink_count=blink_count)
        return table
    
    # recursive case
    else:
        blink_count += 1
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
        
        return cache_a_stone(initial_stone, stones=split_stones, table=table, blink_count=blink_count)


def cache_all_stones():
    table = {}
    for initial_stone in range(0,10):
        table = cache_a_stone(initial_stone, stones=[initial_stone], table=table, blink_count=0)
    return table

def calc_n_stones_dp(n_blinks, stones : list, table : Mapping[int, CachedStone], blink_count : int = 0, final_stones : list = []):
    
    if blink_count > n_blinks:
        final_stones.extend(stones)
        return final_stones
    
    else:
        split_stones = []
        for stone in stones:
            print(blink_count, stone)
            if stone in table and table[stone].blink_count <= (n_blinks - blink_count):
                blink_count += table[stone].blink_count
                split_stones.extend( table[stone].split_stones )
                
            else:
                blink_count += 1

                if stone == 0:
                    split_stones.append(1)
            
                elif len(str(stone)) % 2 == 0:
                    start = 0
                    end = len(str(stone))
                    half = (start + end ) // 2
                    
                    split_stones.append( int(str(stone)[start:half]) )
                    
                    split_stones.append( int(str(stone)[half:end]) )

                else:
                    split_stones.append( stone * 2024 )

            # insert the result of stone decomposition to the split stones for the i-th stone all the way to nth blinks
            final_stones.extend(calc_n_stones_dp(n_blinks, stones=split_stones, table=table, blink_count=blink_count, final_stones=final_stones))

    return final_stones

if __name__ == "__main__":
    content = read_file("input.txt")
    stones : List[int] = processing(content)
    split_stones = calc_n_stones(1, 25, stones)
    
    print("Part a:", len(split_stones))

    cache = cache_a_stone(2, [2], {})
    print(cache)
    table = cache_all_stones()
    # print(table)
    split_stones = calc_n_stones_dp(n_blinks=75, stones=[2], table=table, blink_count=0, final_stones=[])
    print(split_stones)
    # print("Part b:", len(split_stones))