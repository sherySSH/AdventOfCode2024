from enum import Enum
from dataclasses import dataclass, field
from typing import Union, List
from copy import deepcopy

class Direction(str, Enum):
    top = '^'
    right = '>'
    left = '<'
    bottom = 'v'

class Blocker(str, Enum):
    block = '#'
    obstruction = 'O'

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


@dataclass
class Node:
    position : Position
    edge_vists : int


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
            

def get_position(orientation : tuple) -> Position:
    position = orientation[0]
    return position

def get_direction(orientation : tuple) -> Direction:
    direction = orientation[1]
    return direction

def search_top(grid, guard_position : Position, positions : list, location_count = 0):
    
    next_position = Position(x=guard_position.x, y=guard_position.y - 1)
    # print(guard_position, next_position)
    if next_position.y < 0:
        return Location(
                        location_count = location_count,
                        position=guard_position,
                        position_history=positions,
                        direction = None
                        )

    elif grid[next_position.y][next_position.x] == Blocker.block or grid[next_position.y][next_position.x] == Blocker.obstruction:
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

    elif grid[next_position.y][next_position.x] == Blocker.block or grid[next_position.y][next_position.x] == Blocker.obstruction:
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

    elif grid[next_position.y][next_position.x] == Blocker.block or grid[next_position.y][next_position.x] == Blocker.obstruction:
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
    
    elif grid[next_position.y][next_position.x] == Blocker.block or grid[next_position.y][next_position.x] == Blocker.obstruction:
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
    """
    Parameters:

    position_list : This is the position history of guard that we will keep updating as we traverse our grid/graph
    
    """
    orientation = get_guard_orientation(grid)
    position = get_position(orientation)
    direction = get_direction(orientation)
 
    if direction == Direction.top:
        location : Location = search_top(grid, position, [], location_count)

    elif direction == Direction.right:
        location : Location = search_right(grid, position, [], location_count)
    
    elif direction == Direction.bottom:
        location : Location = search_bottom(grid, position, [], location_count)
    
    elif direction == Direction.left:
        location : Location = search_left(grid, position, [], location_count)

    # update direction
    direction = location.direction
    # update total location count including overlapping
    location_count = location.location_count
    # get updated position
    updated_position = location.position
    # update position history that was travelled by guard
    position_list.extend(location.position_history)
    
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

def remove_guard_starting_location(starting_pos : Position, positions : List[Position]):
    prep_poisitions = []
    for position in positions:
        if position != starting_pos:
            prep_poisitions.append(position)
    return prep_poisitions

def create_graph(grid):
    graph = {}
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            position = Position(x=x,y=y)
            # add node in the graph if not already present
            if (x,y) not in graph and grid[y][x] != Blocker.block:
                graph[(x,y)] = []
            # if given node is blocker then no need to add it in the graph
            else:
                continue
            
            # add top node if it exists
            if (y-1) >=0 and grid[y-1][x] != Blocker.block:
                graph[(x,y)].append(Node(position=Position(x=position.x, y=position.y-1) ,edge_vists=0))
            # add right node if it exists
            if (x+1) < len(grid[y]) and grid[y][x+1] != Blocker.block:
                graph[(x,y)].append(Node(position=Position(x=position.x+1, y=position.y), edge_vists=0))
            # add bottom node if it exists
            if (y+1) < len(grid) and grid[y+1][x] != Blocker.block:
                graph[(x,y)].append(Node(position=Position(x=position.x , y=position.y+1), edge_vists=0))
            # add left node if it exists
            if (x-1) >=0 and grid[y][x-1] != Blocker.block:
                graph[(x,y)].append(Node(position=Position(x=position.x-1, y=position.y), edge_vists=0))
    return graph

def update_graph(graph, node_i_pos : Position, node_j_pos : Position):
    # if any node position is missing then we cannot determine edge,
    # hence retru the graph as it is without mutation
    if node_i_pos == None or node_j_pos == None:
        return graph
    # since graph is directed therefore we can traverse in just 1 direction at a time
    nodes : List[Node] = graph[(node_i_pos.x,node_i_pos.y)]
    # BFS to find the node_j neighbour
    for node in nodes:
        if node_j_pos == node.position:
            node.edge_vists += 1

    return graph

def detect_infinite_cycle(graph, prev_position, current_position, next_position):
    if prev_position == None or current_position == None or next_position == None:
        return False
    
    # get edge count between previous node and current node
    neighbours : List[Node] = graph[(prev_position.x,prev_position.y)]

    for neighbour in neighbours:
        if neighbour.position == current_position:
            edge_i_count = neighbour.edge_vists
            break
    
    # get edge count between current node and next node
    neighbours : List[Node] = graph[(current_position.x,current_position.y)]
    for neighbour in neighbours:
        if neighbour.position == next_position:
            edge_j_count = neighbour.edge_vists
            break

    if edge_i_count == 1 and edge_j_count == 1:
        return True
    else:
        return False

def get_next_position(i : int, positions : List[Position]):
    if (i+1) < len(positions):
        return positions[i+1]
    else:
        return None
    
def get_prev_position(i : int, positions : List[Position]):
    if (i-1) >= 0:
        return positions[i-1]
    else:
        return None

def place_obstruction(grid : list, position : Position):
    grid[position.y][position.x] = 'O'
    return grid


def search_grid_with_cycle_detection(graph : dict, grid : list, position_list : list, location_count = 1, node_i : int = 0):
    orientation = get_guard_orientation(grid)
    position = get_position(orientation)
    direction = get_direction(orientation)


    if direction == Direction.top:
        location : Location = search_top(grid, position, [], location_count)

    elif direction == Direction.right:
        location : Location = search_right(grid, position, [], location_count)
    
    elif direction == Direction.bottom:
        location : Location = search_bottom(grid, position, [], location_count)
    
    elif direction == Direction.left:
        location : Location = search_left(grid, position, [], location_count)

    # update direction
    direction = location.direction
    
    # update total location count including overlapping
    location_count = location.location_count
    # get updated position
    updated_position = location.position
    # update position history that was travelled by guard
    position_list.extend(location.position_history)
    # update the edge visit counts that are traversed during search
    
    for i in range(node_i, len(position_list)):
        current_position = position_list[i]
        next_position = get_next_position(i, position_list)
        prev_position = get_prev_position(i, position_list)
        has_cycle = detect_infinite_cycle(graph, prev_position, current_position, next_position)
        if has_cycle:
            return True
        else:
            graph = update_graph(graph, current_position, next_position)
    
    node_i = len(position_list) - 1

    # base case that triggers when guard left the patrol area
    if direction == None:
        return False
    # otherwise keep searching for distinct location
    else:
        # update grid
        grid[position.y][position.x] = '.'
        grid[updated_position.y][updated_position.x] = direction.value
        
        return search_grid_with_cycle_detection(graph, grid, position_list, location_count=location_count, node_i=node_i)
    

def count_inifinite_cycles_after_obstruction(grid : list, positions : list):
    # place obstructions
    
    cycle_count = 0
    # remove the starting position of guard from traversed position list
    guard_starting_pos = positions[0]
    obst_positions = remove_guard_starting_location(guard_starting_pos, positions)
    i=0
    # obst_positions = [Position(x=104, y=81)]
    for obst_pos in obst_positions:
        print(f"Obsctruction No. : {i}, Obstruction Position : {obst_pos}")

        grid_copy = deepcopy(grid)
        grid_copy = place_obstruction(grid_copy, obst_pos)
        graph = create_graph(grid_copy)

        # detect cycle
        contains_cycle : bool = search_grid_with_cycle_detection(
                                    graph, 
                                    grid_copy, 
                                    position_list=[get_position(get_guard_orientation(grid_copy))] ,
                                    location_count=1,
                                    node_i=0 
                                    )
        # count cycle
        if contains_cycle:
            cycle_count += 1
        i += 1
        
        print(f"Cumulative Cycle Count : {cycle_count}")
    return cycle_count

if __name__ == "__main__":
    content = read_file("input.txt")
    grid = processing(content)
    position_list = search_grid(
                                deepcopy(grid), 
                                position_list=[get_position(get_guard_orientation(grid))] , 
                                location_count=1
                                )
    
    print("Part a: ", len(get_distint_positions(position_list)) )
   
    cycle_count = count_inifinite_cycles_after_obstruction(grid, get_distint_positions(position_list))
    print("Part b: ", cycle_count)