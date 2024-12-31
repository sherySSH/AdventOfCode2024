from typing import List
import functools

def read_file(path : str):
    with open(path, 'r') as f:
        content = f.read()
    return content

def processing(content : str):
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

@functools.cache()
def calc_n_stones_dp(blink_count : int, n_blinks : int, stones : list, table : dict):

    # base case
    if blink_count > n_blinks:
        return stones
    
    elif tuple(stones) in table:
        pass
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
        
        table[tuple(stones)] = split_stones
        blink_count += 1
        return calc_n_stones(blink_count, n_blinks, split_stones)

if __name__ == "__main__":
    content = read_file("input.txt")
    stones = processing(content)
    split_stones = calc_n_stones(1, 25, stones)
    
    print("Part a:", len(split_stones))

    split_stones = calc_n_stones_dp(1, 75, stones)
    
    print("Part b:", len(split_stones))