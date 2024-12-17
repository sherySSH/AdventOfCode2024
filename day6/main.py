from enum import Enum
from dataclasses import dataclass, field
from typing import Union

class Direction(str, Enum):
    top = '^'
    right = '>'
    left = '<'
    bottom = 'v'

class Blocker(str, Enum):
    block = '#'

@dataclass
class Position():
    x : int
    y : int

class PositionDeltaTable():

    table : dict =  {
            Direction.top : Direction.right,
            Direction.right : Direction.bottom,
            Direction.left : Direction.top,
            Direction.bottom : Direction.left
    }

    def __init__(self):
        pass
        

@dataclass
class Location():
    location_count : int
    position : Position
    position_history : list
    direction : Union[Direction, None]

def read_file(path : str):
    with open(path, 'r') as f:
        content = f.read()
    return content

def processing(content : str):
    lines = content.split("\n")
    grid = [list(line) for line in lines]
    return grid

def get_guard_orientation(grid : list):

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == Direction.top:
                position = Position(x=x, y=y)
                return (position, Direction.top)
            
            elif grid[y][x] == Direction.right:
                position = Position(x=x, y=y)
                return (position, Direction.right)
            
            elif grid[y][x] == Direction.left:
                position = Position(x=x, y=y)
                return (position, Direction.left)
            
            elif grid[y][x] == Direction.bottom:
                position = Position(x=x, y=y)
                return (position, Direction.bottom)
            

def get_position(orientation : tuple):
    position = orientation[0]
    return position

def get_direction(orientation : tuple):
    direction = orientation[1]
    return direction

def search_top(grid, guard_position : Position, positions : list, location_count = 0):
    
    next_position = Position(x=guard_position.x, y=guard_position.y - 1)

    if next_position.y < 0:
        return Location(
                        location_count = location_count,
                        position=guard_position,
                        position_history=positions,
                        direction = None
                        )

    elif grid[next_position.y][next_position.x] == Blocker.block:
        return Location(
                        location_count = location_count, 
                        position=guard_position,
                        position_history=positions,
                        direction = PositionDeltaTable.table[Direction.top]
                        )
    else:
        location_count = location_count + 1
        positions.append(next_position)
        return search_top(grid, next_position, positions, location_count)

def search_right(grid, guard_position : Position, positions : list, location_count = 0):
    next_position = Position(x=guard_position.x + 1, y=guard_position.y)

    if next_position.x >= len(grid[next_position.y]):
        return Location(
                        location_count = location_count,
                        position=guard_position,
                        position_history=positions,
                        direction = None
                        )

    elif grid[next_position.y][next_position.x] == Blocker.block:
        return Location(
                        location_count = location_count,
                        position=guard_position,
                        position_history=positions,
                        direction = PositionDeltaTable.table[Direction.right]
                        )
    else:
        location_count = location_count + 1
        positions.append(next_position)
        return search_right(grid, next_position, positions, location_count)

def search_bottom(grid, guard_position : Position, positions : list, location_count = 0):
    next_position = Position(x=guard_position.x, y=guard_position.y + 1)

    if next_position.y >= len(grid):
        return Location(
                        location_count = location_count,
                        position=guard_position,
                        position_history=positions,
                        direction = None
                        )

    elif grid[next_position.y][next_position.x] == Blocker.block:
        return Location(
                        location_count = location_count,
                        position=guard_position,
                        position_history=positions,
                        direction = PositionDeltaTable.table[Direction.bottom]
                        )

    else:
        location_count = location_count + 1
        positions.append(next_position)
        return search_bottom(grid, next_position, positions, location_count)

def search_left(grid, guard_position : Position, positions : list , location_count = 0):
    next_position = Position(x=guard_position.x - 1, y=guard_position.y)
    
    if next_position.x < 0:
        return Location(
                        location_count = location_count, 
                        position=guard_position,
                        position_history=positions,
                        direction = None
                        )
    
    elif grid[next_position.y][next_position.x] == Blocker.block:
        return Location(
                        location_count = location_count,
                        position=guard_position,
                        position_history=positions,
                        direction = PositionDeltaTable.table[Direction.left]
                        )
    
    else:
        location_count = location_count + 1
        positions.append(next_position)
        return search_left(grid, next_position, positions, location_count)


def search_grid(grid, position_list : list, location_count = 1):
    orientation = get_guard_orientation(grid)
    position = get_position(orientation)
    direction = get_direction(orientation)
 
    if direction == Direction.top:
        location : Location = search_top(grid, position, position_list, location_count)

    elif direction == Direction.right:
        location : Location = search_right(grid, position, position_list, location_count)
    
    elif direction == Direction.bottom:
        location : Location = search_bottom(grid, position, position_list, location_count)
    
    elif direction == Direction.left:
        location : Location = search_left(grid, position, position_list, location_count)

    # update direction
    direction = location.direction
    # update total location count including overlapping
    location_count = location.location_count
    # get updated position
    updated_position = location.position
    # update position history that was travelled by guard
    position_list = location.position_history
    
    # base case that triggers when guard left the patrol area
    if direction == None:
        return position_list
    # otherwise keep searching for distinct location
    else:
        # update grid
        grid[position.y][position.x] = '.'
        grid[updated_position.y][updated_position.x] = direction.value
        # print(position_list)
        return search_grid(grid, position_list, location_count=location_count)


def get_distint_positions(position_list : list):
    distinct_positions = []
    for position in position_list:
        if position not in distinct_positions:
            distinct_positions.append(position)

    return distinct_positions

if __name__ == "__main__":
    content = read_file("input.txt")
    grid = processing(content)
    position_list = search_grid(
                                grid, 
                                position_list=[get_position(get_guard_orientation(grid))] , 
                                location_count=1
                                )
    
    print("Part a: ", len(get_distint_positions(position_list)) )