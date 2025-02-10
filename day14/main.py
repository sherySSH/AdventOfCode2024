import os
from dataclasses import dataclass
from typing import List
import re

@dataclass
class Position:
    x : int
    y : int

@dataclass
class Velocity:
    x : int
    y : int

@dataclass
class Robot:
    pos : Position
    vel : Velocity

def read_file(filepath : str):
    with open(filepath, 'r') as f:
        content = f.read()
    return content

def processing(content : str):
    lines = content.splitlines()
    return lines


def create_grid(grid_x : int, grid_y : int) -> List[List[str]]:
    grid = []
    for y in range(grid_y):
        line = []
        for x in range(grid_x):
            line.append(".")
        grid.append(line)

    return grid

def output_grid(filepath : str, grid : List[List[str]]):    
    folder_path =  os.path.sep.join(os.path.split(filepath)[0:-1])

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, mode=777, exist_ok=True)

    with open(filepath, 'w') as f:
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                f.write(grid[y][x])
            f.write("\n")
        f.close()
    

def create_robot(config : str):
    config_re = re.compile("-?[0-9]+")
    config : List[str] = config_re.findall(config)
    robot = Robot(
                    pos=Position(x=int(config[0]) , y=int(config[1])),
                    vel=Velocity(x=int(config[2]) , y=int(config[3]))
                )
    return robot


def create_robots(configs : List[str]) -> List[Robot]:
    robots : List[Robot] = []
    for config in configs:
        robot = create_robot(config)
        robots.append(robot)
    
    return robots

def insert_robots_into_grid(grid : List[List[str]] , robots : List[Robot]):
    for robot in robots:
        grid[robot.pos.y][robot.pos.x] = "*"
    return grid

def estimate_positions(robots : List[Robot], grid_x = 101, grid_y = 103, seconds=100):
    for second in range(seconds):
        grid = create_grid(grid_x=101, grid_y=103)
        for robot in robots:
            robot.pos.x += robot.vel.x
            robot.pos.y += robot.vel.y
            
            # teleport to other side
            if robot.pos.x < 0:
                robot.pos.x = robot.pos.x + grid_x
            elif robot.pos.x >= grid_x:
                robot.pos.x = robot.pos.x - grid_x

            # teleport to other side
            if robot.pos.y < 0:
                robot.pos.y = robot.pos.y + grid_y
            elif robot.pos.y >= grid_y:
                robot.pos.y = robot.pos.y - grid_y

        grid = insert_robots_into_grid(grid, robots)
        output_grid(os.path.join("snapshots",f"{second}.txt") , grid)

    return robots

def estimate_safety_factor(robots : List[Robot] , grid_x = 101, grid_y = 103):
    mid_x = grid_x // 2
    mid_y = grid_y // 2
    quadrants = { 1 : 0, 2 : 0, 3 : 0, 4 : 0}
    for robot in robots:
        # first quadrant
        if robot.pos.x < mid_x and robot.pos.y < mid_y:
            quadrants[1] += 1
        # second quadrant
        elif robot.pos.x > mid_x and robot.pos.y < mid_y:
            quadrants[2] += 1
        # third quadrant
        elif robot.pos.x < mid_x and robot.pos.y > mid_y:
            quadrants[3] += 1
        # fourth quadrant
        elif robot.pos.x > mid_x and robot.pos.y > mid_y:
            quadrants[4] += 1

    safety_factor = quadrants[1]*quadrants[2]*quadrants[3]*quadrants[4]
    return safety_factor

if __name__ == "__main__":
    content = read_file("input.txt")
    lines = processing(content)
    robots = create_robots(lines)
    robots = estimate_positions(robots)
    safety_factor = estimate_safety_factor(robots)
    print("Part a:", safety_factor)

    
    