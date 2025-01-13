from dataclasses import dataclass
from typing import List
from queue import Queue

@dataclass
class Node:
    value : int
    perimeter : int
    region : int

@dataclass
class Position:
    x : int
    y : int

def read_file(path : str) -> str:
    with open(path, 'r') as f:
        content = f.read()

    return content

def processing(content : str):
    lines : List[str] = content.split("\n")
    grid = []
    for line in lines:
        row : List[str] = []
        for value in list(line):
            node = Node(value=value, perimeter=None, region=None)
            row.append(node)
        grid.append(row)
    
    return grid


def search_grid(grid, direction, current_pos : Position):
    if direction == 'top':
        if (current_pos.y-1) >=0:
            return  Position(x=current_pos.x, y=current_pos.y-1)
        else:
            return None
        
    elif direction == 'right':
        if (current_pos.x+1) < len(grid[current_pos.y]):
            return  Position(x=current_pos.x+1, y=current_pos.y)
        else:
            return None
    
    elif direction == 'bottom':
        if (current_pos.y+1) < len(grid):
            return  Position(x=current_pos.x, y=current_pos.y+1)
        else:
            return None
        
    elif direction == 'left':
        if (current_pos.x-1) >= 0:
            return  Position(x=current_pos.x-1, y=current_pos.y)
        else:
            return None


def update_queue_for_perimeter(grid : List[List[Node]], queue : list, children : list, child_pos : Position):
    if child_pos != None:
            children.append(child_pos)
            # only add that node to queue whose perimeter needs to be calculated
            if grid[child_pos.y][child_pos.x].perimeter == None and child_pos not in queue:
                queue.append(child_pos)
    
    return children, queue

def calc_perimeter(grid : List[List[Node]], queue : list):
    new_queue = []

    if len(queue) == 0:
        return grid

    for _ in range(len(queue)):
        children = [] # default value
        perimeter = 4 # default value
        current_pos : Position = queue.pop(0)
        # search top side
        child_pos : Position = search_grid(grid, direction='top', current_pos=current_pos)
        children, new_queue = update_queue_for_perimeter(grid, new_queue, children, child_pos)
        # search right side
        child_pos : Position = search_grid(grid, direction='right', current_pos=current_pos)
        children, new_queue = update_queue_for_perimeter(grid, new_queue, children, child_pos)
        # search bottom side
        child_pos : Position = search_grid(grid, direction='bottom', current_pos=current_pos)
        children, new_queue = update_queue_for_perimeter(grid, new_queue, children, child_pos)
        # search left side
        child_pos : Position = search_grid(grid, direction='left', current_pos=current_pos)
        children, new_queue = update_queue_for_perimeter(grid, new_queue, children, child_pos)

        # update perimeter
        child : Position
        for child in children:
            if grid[child.y][child.x].value == grid[current_pos.y][current_pos.x].value:
                perimeter = perimeter - 1
        
        # set the value of a perimeter for a current Node
        grid[current_pos.y][current_pos.x].perimeter = perimeter 

    return calc_perimeter(grid, new_queue)

def mark_region(grid, queue_p1 : list, queue_p2 : list):
    """
    queue_p1 is the Priority 1 queue
    queue_p2 is the Priority 2 queue

    Priority importance is:
    1 has higher priority than 2
    """
    
    pass

if __name__ == "__main__":
    content = read_file("input.txt")
    grid = processing(content)
    queue = [ Position(x=0,y=0) ]
    
    grid = calc_perimeter(grid, queue)
    print(grid)
    