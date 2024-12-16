from enum import Enum
from dataclasses import dataclass

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

@dataclass
class PositionDeltaTable():
    table : dict = {
        Direction.top : Direction.right,
        Direction.right : Direction.bottom,
        Direction.left : Direction.top,
        Direction.bottom : Direction.left
    }

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

def search_top(grid, guard_position : Position, location_count = 0):
    
    next_position = Position(x=guard_position.x, y=guard_position.y - 1)

    if grid[next_position.y][next_position.x] == Blocker.block:
        return location_count
    elif next_position.y >= len(grid) and next_position.x >= len(grid[next_position.y]):
        return location_count
    else:
        location_count = location_count + 1
        return search_top(grid, next_position, location_count)

def search_right(grid, guard_position : Position):
    next_position = Position(x=guard_position.x + 1, y=guard_position.y)

    if grid[next_position.y][next_position.x] == Blocker.block:
        return location_count
    elif next_position.y >= len(grid) and next_position.x >= len(grid[next_position.y]):
        return location_count
    else:
        location_count = location_count + 1
        return search_top(grid, next_position, location_count)

def search_bottom(grid, guard_position : Position):
    next_position = Position(x=guard_position.x, y=guard_position.y + 1)

    if grid[next_position.y][next_position.x] == Blocker.block:
        return location_count
    elif next_position.y >= len(grid) and next_position.x >= len(grid[next_position.y]):
        return location_count
    else:
        location_count = location_count + 1
        return search_top(grid, next_position, location_count)

def search_left(grid, guard_position : Position):
    next_position = Position(x=guard_position.x - 1, y=guard_position.y)

    if grid[next_position.y][next_position.x] == Blocker.block:
        return location_count
    elif next_position.y >= len(grid) and next_position.x >= len(grid[next_position.y]):
        return location_count
    else:
        location_count = location_count + 1
        return search_top(grid, next_position, location_count)

if __name__ == "__main__":
    content = read_file("input.txt")
    grid = processing(content)
    print(grid)
    orientation = get_guard_orientation(grid)
    