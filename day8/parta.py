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


def create_antinode(grid_x : int, grid_y : int, antenna_pair : AntennaPair) -> AntinodePair:
    antinode_pair = AntinodePair(None, None)
    
    diff_x = antenna_pair.i.x - antenna_pair.j.x
    diff_y = antenna_pair.i.y - antenna_pair.j.y

    antinode_i = Position( 
                        x=antenna_pair.i.x - 2*diff_x , 
                        y=antenna_pair.i.y - 2*diff_y
                        )

    diff_x = antenna_pair.j.x - antenna_pair.i.x
    diff_y = antenna_pair.j.y - antenna_pair.i.y

    antinode_j = Position(
                          x=antenna_pair.j.x - 2*diff_x,
                          y=antenna_pair.j.y - 2*diff_y
                        )
    # count antinode only if it lies within the bounds of the grid
    if is_antinode_bounded(grid_x, grid_y, antinode_i):
        antinode_pair.i = antinode_i
    if is_antinode_bounded(grid_x, grid_y, antinode_j):
        antinode_pair.j = antinode_j

    return antinode_pair
    

def is_antinode_bounded(grid_x : int, grid_y : int, antinode : Position):
    # if antinode lies outside the grid then return False
    if antinode.x >= grid_x or antinode.y >= grid_y or antinode.x < 0 or antinode.y < 0:
        return False
    else:
        return True

def create_antinodes(grid_x : int, grid_y : int, freq_pairs : dict):
    antinode_pairs : list = []    
    for freq in freq_pairs:
        antenna_pairs : list = freq_pairs[freq]
        for pair in antenna_pairs:
            antinode_pair : AntinodePair = create_antinode(grid_x, grid_y, pair)
            antinode_pairs.append(antinode_pair)
    return antinode_pairs


def flatten_antinode_pairs(antinode_pairs : List[AntinodePair]):
    antinodes : list = []
    pair : AntinodePair
    for pair in antinode_pairs:
        # if antinode is duplicate then we do not count it
        # if antinode lies outside the bounds of grid we do not consider it

        if pair.i not in antinodes and pair.i is not None:
            antinodes.append(pair.i)

        if pair.j not in antinodes and pair.j is not None:
            antinodes.append(pair.j)
    
    return antinodes

if __name__ == "__main__":
    content = read_file('input.txt')
    grid = preprocessing(content)
    antennas = get_antennas(grid)

    antennas : Mapping[str, List[tuple]] = drop_single_antenna(antennas)
    freq_pairs : Mapping[str, List[AntinodePair]] = create_pairs_for_all_freqs(antennas)

    antinode_pairs : List[AntinodePair] = create_antinodes(len(grid) , len(grid[0]), freq_pairs)
    antinodes : list = flatten_antinode_pairs(antinode_pairs)

    print("Part a:",len(antinodes))
    