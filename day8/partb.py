import os
from typing import List, Union, Callable, Mapping
import re
from dataclasses import dataclass


@dataclass
class Position:
    x : int
    y : int

@dataclass
class AntennaPair:
    i : Position
    j : Position

@dataclass
class AntinodePair:
    i : Position
    j : Position

def read_file(path : str):
    with open(path, 'r') as f:
        content = f.read()
    return content

def preprocessing(content : str) -> tuple:
    grid = []
    lines = content.split("\n")
    for line in lines:
        grid.append( tuple(line) )

    grid = tuple(grid)
    return grid

def get_antennas(grid : tuple):
    antennas : Mapping[str,List[tuple]] = {}  
    antenna = re.compile('[0-9]|[a-zA-Z]')
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            element = grid[y][x]
            if element not in antennas and antenna.match(element) != None:
                antennas[ element ] = [(x,y)]
            elif antenna.match(element) != None:
                antennas[ element ].append((x,y))
    return antennas

def drop_single_antenna( antennas : Mapping[str,List[tuple]]):
    for freq in antennas:
        if len(antennas) == 1:
            del antennas[freq]
    return antennas


def create_antenna_pair(antenna_i : tuple, antenna_j : tuple):
    antenna_pair : AntennaPair = AntennaPair(
                                            i=Position(x=antenna_i[0], y=antenna_i[1]),
                                            j=Position(x=antenna_j[0], y=antenna_j[1])
                                            )
    return antenna_pair

def create_antenna_pairs(ith_antenna_list : List[tuple]):
    pairs : List[AntennaPair] = []
    for i in range(len(ith_antenna_list)):
        for j in range(i+1, len(ith_antenna_list)):
            pair = create_antenna_pair(ith_antenna_list[i] , ith_antenna_list[j])
            pairs.append(pair)

    return pairs

def create_pairs_for_all_freqs(antennas: Mapping[str,List[tuple]] ):
    freq_pairs : Mapping[str, List[AntennaPair]] = {}
    for freq in antennas:
        pairs = create_antenna_pairs(antennas[freq])
        freq_pairs[freq] = pairs

    return freq_pairs


def create_antinodes(grid_x : int, grid_y : int, antenna_pair : AntennaPair) -> list:
    """
    NOTE:

    Now Anti-Node can also occur at each antenna present in the same frequency pair.
    In other words, there is not restriction that an Anti-Node must be twice the distance
    between antennas from the one antenna in the pair
    """
    
    antinodes = []

    diff_x = antenna_pair.i.x - antenna_pair.j.x
    diff_y = antenna_pair.i.y - antenna_pair.j.y
    ##### start do while loop ####

    i = 1
    antinode_i = Position( 
                        x=antenna_pair.i.x - i*diff_x , 
                        y=antenna_pair.i.y - i*diff_y
                        )
    
    # count antinode only if it lies within the bounds of the grid
    is_bounded = is_antinode_bounded(grid_x, grid_y, antinode_i)
    while is_bounded:
        antinodes.append(antinode_i)
        i += 1
        antinode_i = Position( 
                        x=antenna_pair.i.x - i*diff_x , 
                        y=antenna_pair.i.y - i*diff_y
                        )
        is_bounded = is_antinode_bounded(grid_x, grid_y, antinode_i)
        
    ##### end do while loop ####


    diff_x = antenna_pair.j.x - antenna_pair.i.x
    diff_y = antenna_pair.j.y - antenna_pair.i.y
    ##### start do while loop ####
    j = 1
    antinode_j = Position(
                          x=antenna_pair.j.x - j*diff_x,
                          y=antenna_pair.j.y - j*diff_y
                        )
    
    is_bounded = is_antinode_bounded(grid_x, grid_y, antinode_j)
    while is_bounded:
        antinodes.append(antinode_j)
        j += 1
        antinode_j = Position(
                          x=antenna_pair.j.x - j*diff_x,
                          y=antenna_pair.j.y - j*diff_y
                        )
        is_bounded = is_antinode_bounded(grid_x, grid_y, antinode_j)
        
    ##### end do while loop ####

    return antinodes
    

def is_antinode_bounded(grid_x : int, grid_y : int, antinode : Position):
    # if antinode lies outside the grid then return False
    if antinode.x >= grid_x or antinode.y >= grid_y or antinode.x < 0 or antinode.y < 0:
        return False
    else:
        return True

def create_antinodes_for_all_freq(grid_x : int, grid_y : int, freq_pairs : dict):
    antinodes : list = []    
    for freq in freq_pairs:
        antenna_pairs : list = freq_pairs[freq]
        for pair in antenna_pairs:
            antinodes.extend( create_antinodes(grid_x, grid_y, pair))
    
    unique_antinodes : list = []
    for antinode in antinodes:
        if antinode not in unique_antinodes:
            unique_antinodes.append(antinode)
    
    return unique_antinodes


if __name__ == "__main__":
    content = read_file('input.txt')
    grid = preprocessing(content)
    antennas = get_antennas(grid)

    antennas : Mapping[str, List[tuple]] = drop_single_antenna(antennas)
    freq_pairs : Mapping[str, List[AntinodePair]] = create_pairs_for_all_freqs(antennas)

    antinodes : List[AntinodePair] = create_antinodes_for_all_freq(len(grid) , len(grid[0]), freq_pairs)

    print("Part b:",len(antinodes))
    