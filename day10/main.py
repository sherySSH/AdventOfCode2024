import os
from typing import List
from dataclasses import dataclass

@dataclass
class Position:
    x : int
    y : int

def read_file(path : str) -> List[str]:
    with open(path, 'r') as f:
        content = f.read()
    return content

def processing(content : str):
    lines = content.split("\n")
    grid = [list(line) for line in lines]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = int(grid[y][x])

    return grid

def get_trailheads(grid : List[List[int]]) -> List[Position]:
    trailheads = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 0:
                trailheads.append(
                    Position(x=x,y=y)
                )
    return trailheads

def search_top(grid : List[List[int]] , trail : List[Position]):
    position  = trail[-1]
    current_height = grid[position.y][position.x]
    if (position.y - 1) >= 0:
        next_height = grid[position.y - 1][position.x]
        slope = next_height - current_height

        # recursive case
        if slope == 1 and next_height != 9:
            trail.append(Position(x=position.x,y=position.y-1))
            return search_top(grid, trail)
        # base case
        elif slope == 1 and next_height == 9:
            trail.append(Position(x=position.x,y=position.y-1))
            return trail
        # base case
        elif slope != 1:
            return trail
    # base case
    else:
        return trail



def search_right(grid : List[List[int]] , trail : List[Position]):
    position  = trail[-1]
    current_height = grid[position.y][position.x]
    if (position.x + 1) < len(grid[position.y]):
        next_height = grid[position.y][position.x + 1]
        slope = next_height - current_height

        # recursive case
        if slope == 1 and next_height != 9:
            trail.append(Position(x=position.x + 1,y=position.y))
            return search_right(grid, trail)
        # base case
        elif slope == 1 and next_height == 9:
            trail.append(Position(x=position.x + 1,y=position.y))
            return trail
        # base case
        elif slope != 1:
            return trail
    # base case
    else:
        return trail


def search_bottom(grid : List[List[int]] , trail : List[Position]):
    position  = trail[-1]
    current_height = grid[position.y][position.x]
    if (position.y + 1) < len(grid):
        
        next_height = grid[position.y + 1][position.x]
        slope = next_height - current_height
        # recursive case
        if slope == 1 and next_height != 9:
            trail.append(Position(x=position.x,y=position.y+1))
            return search_bottom(grid, trail)
        # base case
        elif slope == 1 and next_height == 9:
            trail.append(Position(x=position.x,y=position.y+1))
            return trail
        # base case
        elif slope != 1:
            return trail
    # base case
    else:
        return trail


def search_left(grid : List[List[int]] , trail : List[Position]):
    position  = trail[-1]
    current_height = grid[position.y][position.x]
    if (position.x - 1) >= 0:
        next_height = grid[position.y][position.x - 1]
        slope = next_height - current_height

        # recursive case
        if slope == 1 and next_height != 9:
            trail.append(Position(x=position.x - 1,y=position.y))
            return search_left(grid, trail)
        # base case
        elif slope == 1 and next_height == 9:
            trail.append(Position(x=position.x - 1,y=position.y))
            return trail
        # base case
        elif slope != 1:
            return trail
    # base case
    else:
        return trail

def validate_trail(trail : List[Position]) -> bool:
    if len(trail) == 10:
        return True
    else:
        return False


def search_grid(grid : List[List[int]], trailheads : List[Position]):
    
    trailhead_scores = { trailhead : 0 for trailhead in trailheads}

    for trailhead in trailheads:
        trail = search_top(grid, [trailhead])
        is_trail_found = validate_trail(trail)
        if is_trail_found:
            trailhead_scores[trailhead] += 1

        trail = search_right(grid, [trailhead])
        is_trail_found = validate_trail(trail)
        if is_trail_found:
            trailhead_scores[trailhead] += 1

        trail = search_bottom(grid, [trailhead])
        is_trail_found = validate_trail(trail)
        if is_trail_found:
            trailhead_scores[trailhead] += 1

        trail = search_left(grid, [trailhead])
        is_trail_found = validate_trail(trail)
        if is_trail_found:
            trailhead_scores[trailhead] += 1
        
        


if __name__ == "__main__":
    content = read_file("input.txt")
    grid = processing(content)
    # print(grid)
    trailheads = get_trailheads(grid)
    print(trailheads[0])
    value = search_top(grid, [trailheads[0]])
    print(value)
    value = search_bottom(grid, [trailheads[1]])
    print(value)
    value = search_right(grid, [trailheads[2]])
    print(value)
    value = search_left(grid, [trailheads[0]])
    print(value)
    