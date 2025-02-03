import os
from dataclasses import dataclass
from typing import List
import re

@dataclass
class Button:
    x : int
    y : int

@dataclass
class Position:
    x : int
    y : int

@dataclass
class Claw:
    button_a : Button
    button_b : Button
    prize : Position
    curr_pos : Position


def read_file(filepath : str):
    with open(filepath, 'r') as f:
        content = f.read()
    return content

def processing(content : str):
    lines = content.split("\n")
    re_moveset = re.compile("[\+\-]?[0-9]+")
    
    button_a = None
    button_b = None
    claw_list : List[Claw] = []
    for line in lines:
        if len(line) == 0:
            button_a = None
            button_b = None
        
        # set Button A
        elif button_a == None:
            moveset = re_moveset.findall(line)
            button_a = Button(x=int(moveset[0]) , y=int(moveset[1]))
        # set Button B
        elif button_b == None:
            moveset = re_moveset.findall(line)
            button_b = Button(x=int(moveset[0]) , y=int(moveset[1]))
        # set Prize
        else:
            goal_loc = re_moveset.findall(line)
            prize = Position(x=10000000000000 + int(goal_loc[0]) , y= 10000000000000 + int(goal_loc[1]))
            claw = Claw(
                 button_a=button_a, 
                 button_b=button_b, 
                 prize=prize, 
                 curr_pos=Position(x=0,y=0)
                 )

            claw_list.append(claw)

            button_a = None
            button_b = None

    return claw_list


def estimate_coeffs(claw : Claw):
    x1 = (claw.button_a.x * claw.prize.y - claw.button_a.y * claw.prize.x) / (claw.button_a.x * claw.button_b.y - claw.button_a.y * claw.button_b.x)
    x2 = (claw.prize.x - claw.button_b.x * x1) / claw.button_a.x 
    coeffs = (x1, x2) 
    return coeffs


def estimate_claws(claws : List[Claw]):
    all_coeffs = []
    for claw in claws:
        coeffs = estimate_coeffs(claw)
        if coeffs[0] == int(coeffs[0]) and coeffs[1] == int(coeffs[1]):
            all_coeffs.append(coeffs)

    return all_coeffs


def calc_total_tokens(all_coeffs : List[List]):
    tokens = 0
    for coeffs in all_coeffs:
        if len(coeffs) != 0:
            tokens += 3*coeffs[0] + coeffs[1]
    tokens = int(tokens)
    return tokens

if __name__ == "__main__":
    content = read_file("input.txt")
    claws = processing(content)
    all_coeffs = estimate_claws(claws)
    # print(all_coeffs)
    total_tokens = calc_total_tokens(all_coeffs)
    print("Part b:",total_tokens)