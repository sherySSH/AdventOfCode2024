from typing import List, Mapping
import math
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
    
    # 1st base case
    if initial_stone in stones and len(stones) != 1:
        table[initial_stone] = CachedStone(split_stones=stones, blink_count=blink_count)
        return table
    # 2nd base case
    elif len(str(initial_stone)) != 1 and len(stones) == 10:
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


def cache_all_stones(stones_range = 10):
    table : Mapping[int, CachedStone]= {}
    for initial_stone in range(0,stones_range):
        table = cache_a_stone(initial_stone, stones=[initial_stone], table=table, blink_count=0)
        # for split_stone in table[initial_stone].split_stones:
            # table = cache_a_stone(initial_stone=split_stone, stones=[split_stone], table=table, blink_count=0)

    return table

def calc_n_stones_memoized(n_blinks, stones : list, table : Mapping[int, CachedStone], blink_count : int = 0, n_stones : int = 0):
    
    if blink_count == n_blinks:
        n_stones += len(stones)
        return n_stones, stones
    
    else:
        for stone in stones:
            # for each stone we want to maintain stack of split stones
            # which will be recursively explored in DFS manner
            split_stones = []
            
            if stone in table and table[stone].blink_count <= (n_blinks - blink_count):
                
                split_stones.extend( table[stone].split_stones )
                # this counts how many times we blinked so far
                updated_blink_count = blink_count + table[stone].blink_count

                # insert the result of stone decomposition to the split stones for the i-th stone all the way to nth blinks
                n_stones, split_stones = calc_n_stones_memoized(n_blinks, stones=split_stones, table=table, blink_count=updated_blink_count, n_stones=n_stones)
                # we will arrive at his line when we have completely explored 1 internal node, and now we want to explore the second
                # internal node present at the same level
                # blink_count -= table[stone].blink_count

            else:
                # this counts how many times we blinked so far
                updated_blink_count = blink_count + 1

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

                
                n_stones, split_stones = calc_n_stones_memoized(n_blinks, stones=split_stones, table=table, blink_count=updated_blink_count, n_stones=n_stones)
                # we will arrive at his line when we have completely explored 1 internal node, and now we want to explore the second
                # internal node present at the same level
                # blink_count -= 1

            
            # if stone not in table:
            #     table[stone] = CachedStone(split_stones=split_stones, blink_count=updated_blink_count)

    return n_stones, split_stones


def calc_n_stones_memoized2(n_blinks, stones : list, table : Mapping[int, CachedStone], blink_count_list : list = [], n_stones : int = 0):
    """
    blink_count_list : each edge of tree containes the blink count of a node, this list contains
                       the blink count from each node in the given branch

    n_blinks : specifies total blinks we need to perform from the first level of stones 
               (those stones that are given as input)
    """
    
    

    if  len(blink_count_list) != 0 and sum(blink_count_list) == n_blinks:
        # print(blink_count_list, n_blinks, n_stones)
        n_stones += len(stones)
        return n_stones, table
    
    else:
        for stone in stones:
            # for each stone we want to maintain stack of split stones
            # which will be recursively explored in DFS manner
            split_stones = []
        
            if stone in table and table[stone].blink_count <= (n_blinks - sum(blink_count_list)):
                # print(blink_count_list, n_blinks)
                # updating blink count list, thereby, updating the edges in the branch
                blink_count_list.append(table[stone].blink_count)
                
                split_stones.extend( table[stone].split_stones )

                # insert the result of stone decomposition to the split stones for the i-th stone all the way to nth blinks
                n_stones, table = calc_n_stones_memoized2(n_blinks, stones=split_stones, table=table, blink_count_list=blink_count_list, n_stones=n_stones)
                # we will arrive at his line when we have completely explored 1 internal node, and now we want to explore the second
                # internal node present at the same level
                # blink_count -= table[stone].blink_count
                last_blink_count = blink_count_list.pop()

            else:
                # updating blink count list, thereby, updating the edges in the branch
                blink_count_list.append(1)

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

                
                n_stones, table = calc_n_stones_memoized2(n_blinks, stones=split_stones, table=table, blink_count_list=blink_count_list, n_stones=n_stones)
                # we will arrive at his line when we have completely explored 1 internal node, and now we want to explore the second
                # internal node present at the same level
                # blink_count -= 1
                last_blink_count = blink_count_list.pop()

            # table = cache_a_stone(stone, [stone], table)

    return n_stones, table


def calc_n_stones_memoized3(n_blinks, stones : list, table : Mapping[int, CachedStone], blinks : list, n_stones : int) -> int:
    """
    blink_count_list : each edge of tree containes the blink count of a node, this list contains
                       the blink count from each node in the given branch

    n_blinks : specifies total blinks we need to perform from the first level of stones 
               (those stones that are given as input)
    """

    # if n_blinks have reached then we are left with 0 amounts of stones that have to be splitted
    # hence it is a base case
    if len(stones) == 0:
        return n_stones

    print(max(blinks), min(blinks))
    # new level of stones
    new_stones = []
    # blink counts of new level of stones
    new_blinks = []
    # print(stones, blinks)
    for index, stone in enumerate(stones):
        # if n_blinks have already been reached for a stone 
        # then do not decompose it further
        if blinks[index] == n_blinks:
            n_stones += 1
            continue
        
        # if stone already exist in cached table then fetch the split stones from there
        # instead of calculating them again
        if stone in table and ( table[stone].blink_count + blinks[index]) <= n_blinks:
            split_stones : list = table[stone].split_stones
            prev_blink : int = blinks[index]
            new_stones.extend(split_stones)
            new_blinks.extend( [prev_blink + table[stone].blink_count] * len(split_stones)  )

        elif stone == 0:
            prev_blink : int = blinks[index]
            new_stones.append(1)
            new_blinks.append(prev_blink + 1)
            
        # if number of digits are in power of 2 
        # then the number will ultimately be reduced to single digits after several blinks
        elif (math.log2( len(str(stone)) ) % 2 == 0 or math.log2( len(str(stone)) ) % 2 == 1 ) and len(str(stone)) > 1:
            split_stones = [int(stone) for stone in list(str(stone))]
            new_blink = int( math.log2( len(str(stone)) ) )
            prev_blink : int = blinks[index]

            if (prev_blink + new_blink) <= n_blinks:
                new_stones.extend(split_stones)
                new_blinks.extend( [prev_blink + new_blink] * len(split_stones)  )
            else:
                start = 0
                end = len(str(stone))
                half = (start + end ) // 2
                
                new_stones.append( int(str(stone)[start:half]) )
                new_stones.append( int(str(stone)[half:end]) )

                prev_blink : int = blinks[index]
                new_blinks.append(prev_blink + 1)
                new_blinks.append(prev_blink + 1)

            
        # if number of digits are even
        elif len(str(stone)) % 2 == 0:
            
            start = 0
            end = len(str(stone))
            half = (start + end ) // 2
            
            new_stones.append( int(str(stone)[start:half]) )
            new_stones.append( int(str(stone)[half:end]) )

            prev_blink : int = blinks[index]
            new_blinks.append(prev_blink + 1)
            new_blinks.append(prev_blink + 1)

        else:
            prev_blink : int = blinks[index]
            new_stones.append( stone * 2024 )
            new_blinks.append(prev_blink + 1)

    return calc_n_stones_memoized3(n_blinks, new_stones, table, new_blinks, n_stones)

if __name__ == "__main__":
    content = read_file("input.txt")
    stones : List[int] = processing(content)
    split_stones = calc_n_stones(1, 25, stones)
    
    print("Part a:", len(split_stones))

    cache = cache_a_stone(2, [2], {})
    table = cache_all_stones(stones_range = 10)
    print(table)
    # n_stones, _ = calc_n_stones_memoized2(n_blinks=30, stones=stones, table=table, blink_count_list=[], n_stones=0)
    # print(n_stones)
    n_stones = calc_n_stones_memoized3(n_blinks=25,
                                        stones=stones,
                                        table=table,
                                        blinks=[0]*len(stones),
                                        n_stones=0)
    print("Part b:", n_stones)