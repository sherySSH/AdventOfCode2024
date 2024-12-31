import os
from typing import List
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Position:
    x : int
    y : int

@dataclass
class Node:
    value : int
    visited : bool

def read_file(path : str) -> List[str]:
    with open(path, 'r') as f:
        content = f.read()
    return content

def processing(content : str):
    lines = content.split("\n")
    grid = [list(line) for line in lines]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = Node( value = int(grid[y][x]) , visited = False)

    return grid

def get_trailheads(grid : List[List[Node]]) -> List[Position]:
    trailheads = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x].value == 0:
                trailheads.append(
                    Position(x=x,y=y)
                )
    return trailheads

def search_top(grid : List[List[Node]] , current_position : Position):

    current_height = grid[current_position.y][current_position.x].value
    next_position : Position = None
    # checking grid bound
    if (current_position.y - 1) >= 0 and not grid[current_position.y - 1][current_position.x].visited:
        next_height = grid[current_position.y - 1][current_position.x].value
        slope = next_height - current_height

        if slope == 1:
            next_position = Position(x=current_position.x,y=current_position.y-1)
            grid[current_position.y - 1][current_position.x].visited = True
    
    return next_position



def search_right(grid : List[List[Node]] , current_position : Position):
    
    current_height = grid[current_position.y][current_position.x].value
    next_position : Position = None
    # checking grid bound
    if (current_position.x + 1) < len(grid[current_position.y]) and not grid[current_position.y][current_position.x + 1].visited:
        next_height = grid[current_position.y][current_position.x + 1].value
        slope = next_height - current_height

        if slope == 1:
            next_position = Position(x=current_position.x + 1, y=current_position.y)
            grid[current_position.y][current_position.x + 1].visited = True
    
    return next_position


def search_bottom(grid : List[List[Node]] , current_position : Position):

    current_height = grid[current_position.y][current_position.x].value
    next_position : Position = None
    # checking grid bound
    if (current_position.y + 1) < len(grid) and not grid[current_position.y + 1][current_position.x].visited:
        next_height = grid[current_position.y + 1][current_position.x].value
        slope = next_height - current_height

        if slope == 1:
            next_position = Position(x=current_position.x , y=current_position.y + 1)
            grid[current_position.y + 1][current_position.x].visited = True
    
    return next_position


def search_left(grid : List[List[Node]] , current_position : Position):
    
    current_height = grid[current_position.y][current_position.x].value
    next_position : Position = None
    # checking grid bound
    if (current_position.x - 1) >= 0 and not grid[current_position.y][current_position.x - 1].visited:
        next_height = grid[current_position.y][current_position.x - 1].value
        slope = next_height - current_height
        
        if slope == 1:
            next_position = Position(x=current_position.x - 1, y=current_position.y)
            grid[current_position.y][current_position.x - 1].visited = True
    
    return next_position




def search_grid(grid : List[List[Node]], trail : List[Position], trailhead_score=0):
    
    # base case
    if len(trail) == 0:
        return trailhead_score
    
    # recursive case
    else:
        current_position = trail.pop()
        grid[current_position.y][current_position.x].visited = True

        top_pos = search_top(grid, current_position )
        right_pos = search_right(grid, current_position)
        bottom_pos = search_bottom(grid, current_position)
        left_pos = search_left(grid, current_position)

        # leaf node case
        if top_pos is not None and grid[top_pos.y][top_pos.x].value == 9: trailhead_score += 1
        # internal node case
        elif top_pos is not None: trail.append(top_pos)

        # leaf node case
        if right_pos is not None and grid[right_pos.y][right_pos.x].value == 9: trailhead_score += 1
        # internal node case
        elif right_pos is not None : trail.append(right_pos)

        # leaf node case
        if bottom_pos is not None and grid[bottom_pos.y][bottom_pos.x].value == 9: trailhead_score += 1
        # internal node case
        elif bottom_pos is not None: trail.append(bottom_pos)

        # leaf node case
        if left_pos is not None and grid[left_pos.y][left_pos.x].value == 9: trailhead_score += 1
        # internal node case
        elif left_pos is not None: trail.append(left_pos)

        return search_grid(grid, trail, trailhead_score)
        

def search_over_all_trailheads(grid : List[List[Node]], trailheads : List[Position]):
    sum = 0
    for trailhead in trailheads:
        copy_grid = deepcopy(grid)
        score = search_grid(copy_grid, [trailhead], 0)
        sum += score

    return sum

if __name__ == "__main__":
    content = read_file("input.txt")
    grid = processing(content)
    trailheads = get_trailheads(grid)
    sum = search_over_all_trailheads(grid, trailheads)
    print("Part a:", sum)