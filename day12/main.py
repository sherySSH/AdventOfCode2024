from dataclasses import dataclass
from typing import List
from queue import Queue

@dataclass
class Node:
    value : str
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


def update_queue_for_area(grid : List[List[Node]], parent : Position, queue_p1 : list, queue_p2 : list, child_pos : Position):
    if child_pos != None and grid[child_pos.y][child_pos.x].region == None:
        if grid[child_pos.y][child_pos.x].value == grid[parent.y][parent.x].value:
            grid[child_pos.y][child_pos.x].region = grid[parent.y][parent.x].region
            queue_p1.append(child_pos)
        else:
            queue_p2.append(child_pos)

    return queue_p1, queue_p2

def mark_region(grid : List[List[Node]], queue_p1 : list, queue_p2 : list, region = 0):
    """
    queue_p1 is the Priority 1 queue
    queue_p2 is the Priority 2 queue

    Priority importance is:
    1 has higher priority than 2

    This is a priority algorithm, because it first prioritizes to find the 
    same-valued region of the current node, and only once it had found one
    region of same-valued nodes it will proceed to check the region of differently-valued node
    It does not find all regions together, instead it finds the regions one-by-one.

    Finding 1 region is 1 solution, once it had found 1 solution. Then it proceeds to find other
    region, hence other solution. When all solutions have been found then we can use colored
    nodes to compute the area of region.

    During BFS traverasal, all neighbouring nodes whose value is different from current node
    are placed in queue_p2 (2nd Priority Queue) meanwhile those neighbouring nodes that have
    same valued are placed in queue_p1 (1st Priority Queue). When queue_p1 is empty then it
    means we have discovered 1 region and no nodes are further remain to be explored in that
    region hence that region is concluded/found. Then we pop the node from queue_p2 and place
    in queue_p1 to discover the region of that node.

    Example to Dry Run the implemented algorithm:

    R   R   R   I   I
    V   R   R   V   I
    V   R   I   I   I
    I   O   O   R   R
    """
    
    
    while True:
        new_queue_p1 = []
        while len(queue_p1) != 0:
            current_pos : Position = queue_p1.pop(0)
            # set the value of a perimeter for a current Node
            grid[current_pos.y][current_pos.x].region = region 

            # search top side
            child_pos : Position = search_grid(grid, direction='top', current_pos=current_pos)
            new_queue_p1, queue_p2 = update_queue_for_area(grid, current_pos, new_queue_p1, queue_p2, child_pos)
            # search right side
            child_pos : Position = search_grid(grid, direction='right', current_pos=current_pos)
            new_queue_p1, queue_p2 = update_queue_for_area(grid, current_pos, new_queue_p1, queue_p2, child_pos)
            # search bottom side
            child_pos : Position = search_grid(grid, direction='bottom', current_pos=current_pos)
            new_queue_p1, queue_p2 = update_queue_for_area(grid, current_pos, new_queue_p1, queue_p2, child_pos)
            # search left side
            child_pos : Position = search_grid(grid, direction='left', current_pos=current_pos)
            new_queue_p1, queue_p2 = update_queue_for_area(grid, current_pos, new_queue_p1, queue_p2, child_pos)

        if len(new_queue_p1) == 0 and len(queue_p2) != 0:
            # keep popping nodes from queue_p2 until an uncolored node is found
            # whose region is still needs to be discovered
            current_pos : Position = queue_p2.pop(0)
            while grid[current_pos.y][current_pos.x].region != None and len(queue_p2) != 0:
                current_pos : Position = queue_p2.pop(0)
            
            if len(queue_p2) !=0: new_queue_p1.append( current_pos )
            # now next region would be different
            # in other words, color of upcoming nodes will be different
            region += 1
        
        # loop breaker
        elif len(new_queue_p1) == 0 and len(queue_p2) == 0:
            # when nothing is left to be marked then break and return the grid
            break

        queue_p1 = new_queue_p1

    return grid

def calc_price_parta(grid : List[List[Node]]):
    regions = { }
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            node = grid[y][x]
            if node.region not in regions:
                regions[node.region] = { "area" : 1, "perimeter" : node.perimeter}
            else:
                regions[node.region]["area"] += 1
                regions[node.region]["perimeter"] += node.perimeter

    price = 0
    for region in regions:
        price += regions[region]["area"] * regions[region]["perimeter"]

    return price

if __name__ == "__main__":
    content = read_file("input.txt")
    grid = processing(content)
    queue = [ Position(x=0,y=0) ]
    grid = calc_perimeter(grid, queue)
    grid = mark_region(grid, [ Position(x=0,y=0) ], [])
    price = calc_price_parta(grid)
    print("Part a:", price)
    