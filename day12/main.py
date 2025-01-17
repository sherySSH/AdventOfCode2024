from dataclasses import dataclass
from typing import List, Mapping, Set
from enum import Enum

class Direction(str, Enum):
    L = 'left'
    R = 'right'
    T = 'top'
    B = 'bottom'

@dataclass
class Position:
    x : int
    y : int

    # to make Position object hashable implement __hash__ method
    def __hash__(self):
        return hash((self.x,self.y))

@dataclass
class Node:
    value : str
    perimeter : int
    region : int
    sides : List[Direction]
    non_overlapping_sides_count : int
    parent : List[Position]



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
            node = Node(value=value, 
                        perimeter=None, 
                        region=None, 
                        sides=None, 
                        non_overlapping_sides_count=None,
                        parent=[]
                        )
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


#####################################
########### Part A Starts ###########
#####################################

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

#####################################
########### Part B Starts ###########
#####################################

def is_side_blocked(grid : List[List[Node]], parent : Position, child : Position):
    
    # otherwise try to count sides if node belongs to same region as parent
    if  child is None or grid[parent.y][parent.x].region != grid[child.y][child.x].region:
        return True
    else:
        return False

def is_updated(grid : List[List[Node]], child : Position, queue : list):
    
    # if no neighbouring child exists so return True because we cannot explore
    # something that does not exist
    if child is None or child in queue:
        return True
    # checks if node has already been computed for counting sides
    elif grid[child.y][child.x].sides != None:
        return True
    else:
        return False


def calc_sides(grid : List[List[Node]], queue : List[Position]):
    while True:
        # for each new level create:
        new_queue : List[Position] = []
        # for each new level create:
        total_sides = {}
        while len(queue) != 0:
            current_pos : Position = queue.pop(0)
            sides : List[Direction] = []
            # search top side
            child_pos : Position = search_grid(grid, direction='top', current_pos=current_pos)
            if is_side_blocked(grid, current_pos, child_pos): sides.append(Direction.T)
            if not is_updated(grid, child_pos, new_queue): new_queue.append(child_pos)
            # search right side
            child_pos : Position = search_grid(grid, direction='right', current_pos=current_pos)
            if is_side_blocked(grid, current_pos, child_pos): sides.append(Direction.R)
            if not is_updated(grid, child_pos, new_queue): new_queue.append(child_pos)
            # search bottom side
            child_pos : Position = search_grid(grid, direction='bottom', current_pos=current_pos)
            if is_side_blocked(grid, current_pos, child_pos): sides.append(Direction.B)
            if not is_updated(grid, child_pos, new_queue): new_queue.append(child_pos)
            # search left side
            child_pos : Position = search_grid(grid, direction='left', current_pos=current_pos)
            if is_side_blocked(grid, current_pos, child_pos): sides.append(Direction.L)
            if not is_updated(grid, child_pos, new_queue): new_queue.append(child_pos)
            
            if current_pos not in total_sides:
                total_sides[current_pos] = sides
            elif len(sides) < len(total_sides):
                total_sides[current_pos] = sides 
            else:
                pass
        
        # updating the sides for each node
        pos : Position
        for pos in total_sides:
            grid[pos.y][pos.x].sides = total_sides[pos]

        queue = new_queue


        if len(queue) == 0:
            break

    return grid


def update_queue_for_sides(grid : List[List[Node]], parent : Position, queue_p1 : list, queue_p2 : list, child_pos : Position):
    
    if child_pos != None: 
        child_sides : Set[Direction] = set(grid[child_pos.y][child_pos.x].sides)
        if child_pos in grid[parent.y][parent.x].parent:
            return queue_p1, queue_p2
        elif grid[child_pos.y][child_pos.x].region == grid[parent.y][parent.x].region:
            grid[child_pos.y][child_pos.x].parent.append(parent)
            # calculate union of all prent sides
            parent_sides = []
            for parent_i in  grid[child_pos.y][child_pos.x].parent:
                parent_sides.extend(grid[parent_i.y][parent_i.x].sides)
            # union calculation completed
            parent_sides = set(parent_sides)
            # find unique sides that are not present in parent sides
            sides_count = len(child_sides - parent_sides)
            if grid[child_pos.y][child_pos.x].non_overlapping_sides_count == None:
                grid[child_pos.y][child_pos.x].non_overlapping_sides_count = sides_count
                queue_p1.append(child_pos)
            else:
                grid[child_pos.y][child_pos.x].non_overlapping_sides_count = min(sides_count, grid[child_pos.y][child_pos.x].non_overlapping_sides_count) 

        else:
            queue_p2.append(child_pos)


    return queue_p1, queue_p2




def calc_non_overlap_sides(grid : List[List[Node]], queue_p1 : list, queue_p2 : list,):
    while True:
        new_queue_p1 = []
        
        while len(queue_p1) != 0:
            current_pos : Position = queue_p1.pop(0)
            if grid[current_pos.y][current_pos.x].non_overlapping_sides_count == None:
                grid[current_pos.y][current_pos.x].non_overlapping_sides_count = len(grid[current_pos.y][current_pos.x].sides)

            # search top side
            child_pos : Position = search_grid(grid, direction='top', current_pos=current_pos)
            # updating the queue for making next level for traversal
            new_queue_p1, queue_p2 = update_queue_for_sides(grid, current_pos, new_queue_p1, queue_p2, child_pos)

            # search right side
            child_pos : Position = search_grid(grid, direction='right', current_pos=current_pos)
            # updating the queue for making next level for traversal
            new_queue_p1, queue_p2 = update_queue_for_sides(grid, current_pos, new_queue_p1, queue_p2, child_pos)

            # search bottom side
            child_pos : Position = search_grid(grid, direction='bottom', current_pos=current_pos)
            # updating the queue for making next level for traversal
            new_queue_p1, queue_p2 = update_queue_for_sides(grid, current_pos, new_queue_p1, queue_p2, child_pos)

            # search left side
            child_pos : Position = search_grid(grid, direction='left', current_pos=current_pos)
            # updating the queue for making next level for traversal
            new_queue_p1, queue_p2 = update_queue_for_sides(grid, current_pos, new_queue_p1, queue_p2, child_pos)

        if len(new_queue_p1) == 0 and len(queue_p2) != 0:
            # keep popping nodes from queue_p2 until an uncolored node is found
            # whose region is still needs to be discovered
            current_pos : Position = queue_p2.pop(0)
            while grid[current_pos.y][current_pos.x].non_overlapping_sides_count != None and len(queue_p2) != 0:
                current_pos : Position = queue_p2.pop(0)
            
            if len(queue_p2) !=0: new_queue_p1.append( current_pos )

        # loop breaker
        elif len(new_queue_p1) == 0 and len(queue_p2) == 0:
            # when nothing is left to be marked then break and return the grid
            break

        queue_p1 = new_queue_p1

    return grid


def calc_price_partb(grid : List[List[Node]]):
    regions = {}
    price = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x].region not in regions:
                regions[grid[y][x].region] = { "area" : 1, "sides" : grid[y][x].non_overlapping_sides_count}
            else:
                 regions[grid[y][x].region]["area"] += 1
                 regions[grid[y][x].region]["sides"] += grid[y][x].non_overlapping_sides_count
    
    for region in regions:
        price += regions[region]["area"] * regions[region]["sides"]

    return price

if __name__ == "__main__":
    content = read_file("input.txt")
    grid = processing(content)
    queue = [ Position(x=0,y=0) ]
    grid = calc_perimeter(grid, queue)
    grid = mark_region(grid, [ Position(x=0,y=0) ], [])
    price_a = calc_price_parta(grid)
    print("Part a:", price_a)
    grid = calc_sides(grid, [ Position(x=0,y=0) ])
    grid = calc_non_overlap_sides(grid, [ Position(x=0,y=0) ], [])
    price_b = calc_price_partb(grid)
    print("Part b:", price_b)