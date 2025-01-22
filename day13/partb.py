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


def validate_coeffs(claw : Claw, alpha_list : list, beta_list : list):
    coeffs = []
    for i in range(len(alpha_list)):
        alpha = alpha_list[i]
        beta = beta_list[i]
        rem_x = claw.prize.x - alpha*claw.button_a.x - beta*claw.button_b.x
        rem_y = claw.prize.y - alpha*claw.button_a.y - beta*claw.button_b.y
        if rem_x == 0 and rem_y == 0:
            coeffs.append( (alpha , beta) )

    return coeffs

def estimate_coeffs(claw : Claw):
    alpha_list = []
    beta_list = []
    
    if claw.button_a.x > claw.button_b.x:
        
        alpha = claw.prize.x // claw.button_a.x
        while alpha != 0:
            rem = (claw.prize.x  - alpha*claw.button_a.x ) % claw.button_b.x
            if rem == 0:
                beta = (claw.prize.x  - alpha*claw.button_a.x ) // claw.button_b.x
                alpha_list.append(alpha)
                beta_list.append(beta)

            alpha -= 1

        coeffs = validate_coeffs(claw, alpha_list, beta_list)

    else:
        
        beta = claw.prize.x // claw.button_b.x
        while beta != 0:
            rem = (claw.prize.x  - beta*claw.button_b.x ) % claw.button_a.x
            if rem == 0:
                alpha = (claw.prize.x  - beta*claw.button_b.x ) // claw.button_a.x
                alpha_list.append(alpha)
                beta_list.append(beta)

            beta -= 1

        coeffs = validate_coeffs(claw, alpha_list, beta_list)

    return coeffs


def estimate_claws(claws : List[Claw]):
    all_coeffs = []
    for claw in claws:
        coeffs = estimate_coeffs(claw)
        all_coeffs.append(coeffs)

    return all_coeffs


def calc_total_tokens(all_coeffs : List[List]):
    tokens = 0
    for coeffs in all_coeffs:
        if len(coeffs) != 0:
            tokens += 3*coeffs[0][0] + coeffs[0][1]
    return tokens

if __name__ == "__main__":
    content = read_file("input.txt")
    claws = processing(content)
    all_coeffs = estimate_claws(claws)
    total_tokens = calc_total_tokens(all_coeffs)
    print("Part a:",total_tokens)